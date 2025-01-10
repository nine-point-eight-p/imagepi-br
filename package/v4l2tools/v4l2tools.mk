V4L2TOOLS_VERSION = v4l2copy-only
V4L2TOOLS_SITE = https://github.com/nine-point-eight-p/v4l2tools.git
V4L2TOOLS_SITE_METHOD = git
V4L2TOOLS_GIT_SUBMODULES = yes
V4L2TOOLS_LICENSE = Unlicense

define V4L2TOOLS_BUILD_CMDS
	$(MAKE) CC="$(TARGET_CC)" CXX="$(TARGET_CXX)" LD="$(TARGET_LD)" -C $(@D) v4l2copy
endef

define V4L2TOOLS_INSTALL_TARGET_CMDS
	$(INSTALL) -D -m 0755 $(@D)/v4l2copy $(TARGET_DIR)/usr/bin
endef

$(eval $(generic-package))
