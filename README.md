# imagepi-br

基于 Buildroot 为 [imagepi](https://github.com/Evennaire/imagepi) 构建的自定义系统镜像，能够运行基础版本的图像识别模型（`model.tflite`、`model-int8.tflite`）。最终镜像体积约 96 MB。

这是 2024 年秋 THU CST 嵌入式系统课程大实验的相关内容。

## 整体思路

- 硬件：启用无线网、摄像头。

- 软件：只安装必要的软件包（mjpg-streamer、OpenCV、numpy、tflite-runtime、SSH 等），移除无用的软件包（如 ffmpeg）。

- 内核：移除无用的驱动、加密算法等（特别是以内核模块形式存在的）。

## 项目结构

参考 [Buildroot 外部目录树的推荐结构](https://buildroot.org/downloads/manual/manual.html#outside-br-custom)。

- `board/raspberrypi3/`：与开发板相关的文件。

    - `overlay/`：目标文件系统，包含无线网配置（需要修改无线网配置文件 `/var/lib/iwd/<SSID>.psk`）、模型文件、客户端程序等。

    - `busybox.config`：BusyBox 配置文件。

    - `config.txt`：树莓派启动时使用的配置文件 `boot/config.txt`，基于 Buildroot 目录树下 `board/raspberrypi3/config_3.txt` 修改，启用摄像头。

    - `genimage-raspberrypi3.cfg`：树莓派镜像配置文件，基于 Buildroot 目录树下 `board/raspberrypi3/genimage-raspberrypi3.cfg` 修改，使用 extended 版本的固件。

    - `linux.config`：Linux 配置文件。

    - `post-build.sh`：新增软件包构建后脚本，用于移除冗余 Python 文件（此方法待改进）。

    - `post-image.sh`：镜像构建后脚本，基于 Buildroot 目录树下 `board/raspberrypi3/post-image.sh` 修改，使用此目录下的树莓派镜像配置文件代替原配置文件。

- `configs/`：Buildroot 配置文件。

- `package/`：自定义软件包，包括支持 V4L2 loopback 设备的 mjpg-streamer，提供 TensorFlow 运行时支持的 tflite-runtime，提供 v4l2copy 工具的 v4l2tools。

- `patches/`：软件包补丁，包括一个对于 mjpg-streamer 的修复。

- `Config.in`：引入所有自定义软件包的描述文件（`./package/<pkg-name>/Config.in`）。可通过 `gen_configin.sh` 自动生成。

- `external.desc`：外部目录树的描述。

- `external.mk`：引入所有自定义软件包的构建文件（`<pkg-name>.mk`）。

- `gen_configin.sh`：自动生成 `./Config.in` 的脚本。

- `pre-build.sh`：在构建软件包前运行的脚本，主要任务是修改 Buildroot 目录树中 numpy 的版本（此方法待改进）。

## 如何使用

### 环境

- Host: Ubuntu 20.04, x86-64

    - Buildroot 2021.11

- Target: Raspberry Pi 3

### 构建

1. 在 Buildroot 目录树下，添加 Buildroot 外部目录树（本仓库），并根据 Buildroot 配置文件完成设置：

    ```bash
    make BR2_EXTERNAL=/path/to/br2-external raspberrypi3_imgcls_defconfig
    ```

2. 执行外部目录树下的 `pre-build.sh`：

    ```bash
    /path/to/br2-external/pre-build.sh /path/to/br2
    ```

3. 在 Buildroot 目录树下，构建镜像（job 数量可自行调整）：

    ```bash
    make -j16
    ```

### 烧录

使用 [balenaEtcher](https://etcher.balena.io/) 或 [win32 Disk Imager](https://win32diskimager.org/) 将 Buildroot 目录树下的 `output/images/sdcard.img` 烧录到树莓派。

### 运行

在树莓派上执行 `./run.sh`，开始实验。