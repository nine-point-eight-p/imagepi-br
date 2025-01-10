#!/bin/bash

if [ $# -eq 0 ]; then
	echo "Please give the path to Buildroot source tree."
	exit 1
fi

BUILDROOT_DIR=$1

# Change numpy version to 1.21.6
NUMPY_DIR="${BUILDROOT_DIR}/package/python-numpy"
sed -i '7c PYTHON_NUMPY_VERSION = 1.21.6' ${NUMPY_DIR}/python-numpy.mk
mv ${NUMPY_DIR}/python-numpy.hash ${NUMPY_DIR}/python-numpy.hash.backup # disable hash check
