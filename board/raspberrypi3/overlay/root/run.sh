#!/bin/sh

modprobe v4l2loopback video_nr=1
sleep 1

v4l2copy -W 640 -H 360 -F 30 -f JPEG &
sleep 1

mjpg_streamer -i "input_v4l2loopback.so -d /dev/video1 -f 30" -o "output_http.so -p 8080 -w /usr/share/mjpg-streamer/www" &
sleep 1

python classify_picamera.py --model model.tflite --labels synset_words.txt
