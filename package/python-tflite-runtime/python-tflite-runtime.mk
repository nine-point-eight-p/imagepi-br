################################################################################
#
# python-tflite-runtime
#
################################################################################

PYTHON_TFLITE_RUNTIME_VERSION = 2.13.0
PYTHON_TFLITE_RUNTIME_SITE = https://files.pythonhosted.org/packages/13/cc/73cfc6c19777af19c39a3936c9c78fc37505675d3db88e96ea8af48533f6
PYTHON_TFLITE_RUNTIME_SOURCE = tflite_runtime-2.13.0-cp39-cp39-manylinux2014_armv7l.whl

define PYTHON_TFLITE_RUNTIME_EXTRACT_CMDS
	unzip $(PYTHON_TFLITE_RUNTIME_DL_DIR)/$(PYTHON_TFLITE_RUNTIME_SOURCE) -d $(@D)
endef

define PYTHON_TFLITE_RUNTIME_BUILD_CMDS
endef

define PYTHON_TFLITE_RUNTIME_INSTALL_TARGET_CMDS
	cp -r $(@D)/. $(TARGET_DIR)/usr/lib/python3.9/site-packages/
endef

$(eval $(generic-package))

