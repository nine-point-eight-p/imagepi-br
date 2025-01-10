from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import io
import time
import threading
import numpy as np

from PIL import Image
from tflite_runtime.interpreter import Interpreter

from cv2 import VideoCapture, CAP_V4L, CAP_PROP_BUFFERSIZE
import os
import cv2
import requests
import json
import time
import socketio

server_ip = "192.168.137.1"
sio = socketio.Client()
sio.connect(f"http://{server_ip}:5000")

post_url = f"http://{server_ip}:5000/result"

cap = VideoCapture(1, CAP_V4L) # open v4l2loopback device /dev/video1
cap.set(CAP_PROP_BUFFERSIZE, 3)

ret = False
frame = 0
tmp = 0

labels = None
interpreter = None
camera = None


def getCPUuse():
    return os.popen("top -n1 | awk '/CPU:/ {print $2; exit}'").readline().strip()[:-1]

def getMemuse():
    return os.popen("free -m | grep Mem").readline().strip().split()[2]


def load_labels(path):
    with open(path, 'r') as f:
        return {i: line.strip() for i, line in enumerate(f.readlines())}


def set_input_tensor(interpreter, image):
    tensor_index = interpreter.get_input_details()[0]['index']
    input_tensor = interpreter.tensor(tensor_index)()[0]
    tmp_images = (np.array(image, dtype=np.float32) / 127.5) - 1.0 #input scale
    input_details = interpreter.get_input_details()[0]

    if input_details['dtype'] == np.int8:
        input_scale, input_zero_point = input_details["quantization"]
        input_tensor[:, :] = np.int8(tmp_images / input_scale + input_zero_point)
    else:
        input_tensor[:, :] = tmp_images
        # print(input_tensor[:, :].max(), input_tensor[:, :].min())

def classify_image(interpreter, image, top_k=1):
    """Returns a sorted array of classification results."""
    set_input_tensor(interpreter, image)
    interpreter.invoke()
    output_details = interpreter.get_output_details()[0]
    output = np.squeeze(interpreter.get_tensor(output_details['index']))
  
    # If the model is quantized (uint8 data), then dequantize the results
    if output_details['dtype'] == np.int8:
        scale, zero_point = output_details['quantization']
        output = scale * (output - zero_point)

    ordered = np.argpartition(-output, top_k)
    return [(i, output[i]) for i in ordered[:top_k]]


@sio.on('pi')
def on_message(data):
    print("message received!")
    received_time = time.time()
    idx = data.split(' ')[-1]

    _, height, width, _ = interpreter.get_input_details()[0]['shape']
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(frame_rgb.astype('uint8')).resize((width, height), Image.ANTIALIAS)
    # image = Image.fromarray(frame.astype('uint8')).convert('RGB').resize((width, height), Image.ANTIALIAS)
    # image = Image.fromarray(frame).convert('RGB').resize((width, height), Image.ANTIALIAS)

    results = classify_image(interpreter, image)
    label_id, prob = results[0]
    label_id += 1 # fix label index
    annotate_text = '%s %.2f' % (labels[label_id], prob)
    fps = 1 / (time.time() - received_time)
    cpu = getCPUuse()
    mem = getMemuse()
    data = {"res": labels[label_id], 
            "fps": fps,
            "cpu": cpu,
            "mem": mem,
            "idx": idx}
    res = requests.post(url=post_url,data=data)
    print(data)



def get_frame():
    global ret, frame, tmp
    while True:
        ret, frame = cap.read()
        time.sleep(0.01)


def main():
    global ret, frame, tmp, labels, interpreter, camera
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '--model', help='File path of .tflite file.', required=True)
    parser.add_argument(
        '--labels', help='File path of labels file.', required=True)
    args = parser.parse_args()

    labels = load_labels(args.labels)

    interpreter = Interpreter(args.model)
    interpreter.allocate_tensors()

    while True:
        time.sleep(1)

if __name__ == '__main__':
    t = threading.Thread(target=get_frame)
    t.setDaemon(True)
    t.start()
    main()
