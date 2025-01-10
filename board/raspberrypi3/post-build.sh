# Remove redundant python files
PYTHON_PATH=${TARGET_DIR}/usr/lib/python3.9/
rm -rf ${PYTHON_PATH}/distutils/ ${PYTHON_PATH}/ensurepip/ ${PYTHON_PATH}/turtledemo/ \
	        ${PYTHON_PATH}/unittest/ ${PYTHON_PATH}/turtle.pyc

