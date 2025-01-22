# prepare develop environment

## content

- [ARM](#arm)
  - [GNU Arm Embedded Toolchain](#gnu-arm-embedded-toolchain)
  - [Keil MDK](#keil-mdk)
- [STM32](#stm32)
  - [ST-Link](#st-link)
  - [STM32CubeMX](#stm32cubemx)
  - [STM32CubeProgrammer](#stm32cubeprogrammer)
  - [STM32CubeCLT](#stm32cubeclt)
  - [STM32CubeIDE](#stm32cubeide)
- [other](#other)
  - [VSCode](#vscode)
  - [gdb](#gdb)
  - [OpenOCD](#openocd)
  - [stlink](#stlink)

windows 建議使用 STM32CubeMX + STM32CubeIDE 開發
linux 建議使用 STM32CubeMX + GNU Arm Embedded Toolchain + make + VSCode / VIM 開發
CI/CD 建議使用 STM32CubeCLT

---

## arm

### GNU Arm Embedded Toolchain

GNU Arm Embedded Toolchain 是一套為 ARM 微控制器（包括 STM32 系列）開發的開源工具鏈。它由 GNU Compiler Collection（GCC）、GNU Binutils 和 GNU Debugger（GDB）等工具組成，專為嵌入式開發設計。這些工具用來編譯、鏈接、調試和生成 ARM 架構的執行檔。

[GNU Arm Embedded Toolchain](https://developer.arm.com/downloads/-/arm-gnu-toolchain-downloads)

```bash
# for debian 12
linux:~ # apt install gcc-arm-none-eabi
linux:~ # cp -r /usr/share/doc/gcc-arm-none-eabi/examples/src .

# for binary
linux:~ # tar jxf gcc-arm-none-eabi-10.3-2021.10-x86_64-linux.tar.bz2 -C /usr/local/
linux:~ # ln -s /usr/local/gcc-arm-none-eabi-10.3-2021.10/bin/arm-none-eabi-gcc /usr/local/bin/.
linux:~ # cp -r /usr/local/gcc-arm-none-eabi-10.3-2021.10/share/gcc-arm-none-eabi/samples/src .

# test
linux:~ # cd src
linux:~ # arm-none-eabi-gcc -v
linux:~/src # make -C qemu
```

### Keil MDK

Keil MDK（Microcontroller Development Kit）是一款由 Arm 提供的集成開發環境（IDE），專門為嵌入式開發設計，特別是針對基於 ARM Cortex-M 核心的微控制器（如 STM32、NXP、Texas Instruments 等）的開發。Keil MDK 提供了全面的工具集，幫助開發者快速編寫、編譯、調試和優化嵌入式應用程序。

[MDK-ARM](https://www.keil.com/demo/eval/arm.htm)

---

## STM32

### ST-Link

ST-Link 是由 STMicroelectronics 提供的一系列調試器和編程器，用於 STM32 微控制器的開發。它支持 SWD 和 JTAG 接口進行固件下載、調試和內存讀寫，是 STM32 開發工作流中的關鍵硬體工具。

[ST-LINK](https://www.st.com/en/development-tools/stsw-link009.html)

### STM32CubeMX

STM32CubeMX 是由 STMicroelectronics 提供的一款免費軟體工具，用於配置和初始化 STM32 微控制器的硬體外設。它能生成基於 HAL（Hardware Abstraction Layer）或 LL（Low-Layer API）的 C 代碼，並支持集成到 STM32CubeIDE 或其他 IDE 中進行開發。

[STM32CubeMX](https://www.st.com/en/development-tools/stm32cubemx.html)

```bash
# requirement
linux:~ # apt install openjdk-11-jdk openjdk-11-jdk-headless    # for debian/ubuntu

# for system
linux:~ # unzip en.stm32cubemx-lin-v6-10-0.zip
linux:~ # ./SetupSTM32CubeMX-6.10.0
linux:~ # /usr/local/STMicroelectronics/STM32Cube/STM32CubeMX/STM32CubeMX
linux:~ # ln -s /usr/local/STMicroelectronics/STM32Cube/STM32CubeMX/STM32CubeMX /usr/local/bin/.

# for user
linux:~ $ unzip en.stm32cubemx-lin-v6-10-0.zip
linux:~ $ ./SetupSTM32CubeMX-6.10.0
linux:~ $ ~/STM32CubeMX/STM32CubeMX
```

```powershell
# for system
PS C:\> dir $env:ProgramFiles\STMicroelectronics\STM32Cube\STM32CubeMX
PS C:\> Start-Process $env:ProgramFiles\STMicroelectronics\STM32Cube\STM32CubeMX\STM32CubeMX.exe

# for user
PS C:\> dir $env:USERPROFILE\AppData\Local\Programs\STM32CubeMX
PS C:\> Start-Process $env:USERPROFILE\AppData\Local\Programs\STM32CubeMX\STM32CubeMX.exe
```

---

### STM32CubeProgrammer

STM32CubeProgrammer (STM32CubeProg) 是由 STMicroelectronics 提供的一款多功能工具，用於 STM32 微控制器的固件燒錄、內存管理和設備配置。它支持多種接口（如 ST-LINK、UART、USB DFU 等）進行固件更新，並可用於調試和校準。

[STM32CubeProgrammer](https://www.st.com/en/development-tools/stm32cubeprog.html)

```bash
# for system
linux:~ # unzip en.stm32cubeprg-lin-v2-15-0.zip
linux:~ # ./SetupSTM32CubeProgrammer-2.15.0.linux
linux:~ # /usr/local/STMicroelectronics/STM32Cube/STM32CubeProgrammer/bin/STM32_Programmer_CLI
linux:~ # ln -s /usr/local/STMicroelectronics/STM32Cube/STM32CubeProgrammer/bin/STM32_Programmer_CLI /usr/local/bin/.
```

```powershell
# for windows
PS C:\> dir C:\Program Files\STMicroelectronics\STM32Cube\STM32CubeProgrammer\bin\STM32CubeProgrammer.exe
```

```text
USB:  Universal Serial Bus - ttypUSB
UART: Universal Asynchronous Receiver Transmitter
JTAG: Joint Test Action Group
SWD:  Serial Wire Debug
SPI:  Serial Peripheral Interface
CAN:  Controller Area Network
I2C:  Inter-Integrated Circuit

VPC: Virtual Port Communication
CDC: Communication Device Class
ACM: Abstract Control Model - ttypACM
```

```bash
linux:~ # STM32_Programmer_CLI -h       # help
linux:~ # STM32_Programmer_CLI -l       # list

linux:~ # STM32_Programmer_CLI -c port=SWD -r32 0x08000000 0x400                # read flash
linux:~ # STM32_Programmer_CLI -c port=SWD -r32 0x08000000 0x400 -f <fw>.bin    # read flash to save bin
linux:~ # STM32_Programmer_CLI -c port=SWD -d <fw>.bin 0x08000000 -v            # write flash
linux:~ # STM32_Programmer_CLI -c port=SWD -w <fw>.bin 0x08000000 -v -rst       # write flash
linux:~ # STM32_Programmer_CLI -c port=SWD -e all                               # erase flash

linux:~ # STM32_Programmer_CLI -c port=SWD -hardRst                         # hardware reset
linux:~ # STM32_Programmer_CLI -c port=SWD -rst                             # reset
linux:~ # STM32_Programmer_CLI -c port=SWD -s                               # start
```

### STM32CubeCLT

[STM32CubeCLT](https://www.st.com/en/development-tools/stm32cubeclt.html)

STM32CubeCLT (Command-Line Tool) 是由 STMicroelectronics 提供的一個命令列工具，用於在命令行環境中執行 STM32 相關操作，例如編譯、生成程式碼、下載程式到設備等，適合自動化工作流或無需完整 IDE 支援的情況。

```powershell
# for windows
PS C:\> dir C:\ST\STM32CubeCLT_1.17.0\
├─CMakeCMake
├─drivers
├─GNU-tools-for-STM32
├─jre
├─Ninja
├─STLink-gdb-server
├─STLinkServer
├─STM32CubeProgrammer
├─STM32target-mcu
└─STMicroelectronics_CMSIS_SVD

PS C:\> dir C:\ST\STM32CubeCLT_1.17.0\STM32CubeProgrammer\bin\STM32_Programmer_CLI.exe
```

### STM32CubeIDE

STM32CubeIDE 是由 STMicroelectronics 提供的一款整合開發環境 (IDE)，專為 STM32 微控制器設計。它結合了 STM32CubeMX 的配置功能和 Eclipse 的編輯器，內建 GNU Arm 工具鏈和調試器，適合開發、編譯、調試 STM32 的應用程式。

[STM32CubeIDE](https://www.st.com/en/development-tools/stm32cubeide.html)

```powershell
# for windows
PS C:\> dir C:\ST\STM32CubeIDE_1.17.0\STM32CubeIDE
PS C:\> Start-Process C:\ST\STM32CubeIDE_1.17.0\STM32CubeIDE\stm32cubeide.exe
```

---

## other

### VSCode

[visual studio code](https://code.visualstudio.com/)
[Arm Assembly](https://marketplace.visualstudio.com/items?itemName=dan-c-underwood.arm)
[Cortex-Debug](https://marketplace.visualstudio.com/items?itemName=marus25.cortex-debug)
[C/C++](https://marketplace.visualstudio.com/items?itemName=ms-vscode.cpptools)
[Makefile Tools](https://marketplace.visualstudio.com/items?itemName=ms-vscode.makefile-tools)

```bash
linux:~/STM32CubeMX/proj $ grep -Pzo "C_INCLUDES =[\s\S]+?(\s){2}" Makefile
=>
filled c_cpp_properties.json includePath

linux:~/STM32CubeMX/proj $ grep -Pzo "C_DEFS =[\s\S]+?(\s){2}" Makefile
=>
filled c_cpp_properties.json includePath
```

```json
// C/C++: Edit Configurations (JSON)
// c_cpp_properties.json
{
  "configurations": [
    {
      "name": "Linux",
      "includePath": [
        "${workspaceFolder}/**",
        "./Core/Inc",
        "./Drivers/STM32F7xx_HAL_Driver/Inc",
        "./Drivers/STM32F7xx_HAL_Driver/Inc/Legacy",
        "./Drivers/CMSIS/Device/ST/STM32F7xx/Include",
        "./Drivers/CMSIS/Include"
      ],
      "defines": ["STM32F767xx", "USE_HAL_DRIVER"],
      "compilerPath": "/usr/bin/gcc",
      "cStandard": "c17",
      "cppStandard": "gnu++14",
      "intelliSenseMode": "linux-gcc-x64"
    }
  ],
  "version": 4
}
```

### gdb

```bash
linux:~ # apt install gdb-multiarch

linux:~ # ln -s /usr/bin/gdb-multiarch /usr/local/bin/arm-none-eabi-gdb
```

### OpenOCD

[Open On-Chip Debugger](https://openocd.org/)
[openocd-org / openocd](https://github.com/openocd-org/openocd)

```bash
# for debian12
linux:~ # apt install openocd

# prepare
linux:~ # apt install build-essential
linux:~ # apt make libtool pkg-config autoconf automake texinfo git
# - make
# - libtool
# - pkg-config or pkgconf >= 0.23
# - autoconf >= 2.69
# - automake >= 1.14
# - texinfo >= 5.0
# - git

# for binary
linux:~ # git clone https://github.com/openocd-org/openocd.git
linux:~/openocd # cd openocd
linux:~/openocd # ./bootstrap
linux:~/openocd # ./configure
linux:~/openocd # make
linux:~/openocd # make install
```

```bash
# step 1.
# terminal 1 launch openocd
# OCD_SCRIPT=/usr/share/openocd/scripts
linux:~ # openocd -f $OCD_SCRIPT/interface/stlink-v2.cfg -f $OCD_SCRIPT/target/stm32l4x.cfg

# step 2.
# terminal 2
linux:~ # arm-none-eabi-gdb build/<fw>.elf
(gdb) target remote localhost:3333
Remote debugging using localhost:3333
(gdb) monitor reset
Unable to match requested speed 500 kHz, using 480 kHz
Unable to match requested speed 500 kHz, using 480 kHz
(gdb) monitor halt
[stm32l4x.cpu] halted due to debug-request, current mode: Thread
xPSR: 0x21000000 pc: 0x080002ce msp: 0x20017ff8
(gdb) load
Loading section .isr_vector, size 0x188 lma 0x8000000
Loading section .text, size 0xf70 lma 0x8000188
Loading section .rodata, size 0x40 lma 0x80010f8
Loading section .init_array, size 0x8 lma 0x8001138
Loading section .fini_array, size 0x8 lma 0x8001140
Loading section .data, size 0x10 lma 0x8001148
Start address 0x08001034, load size 4440
Transfer rate: 13 KB/sec, 740 bytes/write.
(gdb) -
```

---

### stlink

[stlink](https://github.com/stlink-org/stlink)

```bash
linux:~ # apt install stlink-tools stlink-gui

# prepare
linux:~ # git make cmake libusb-1.0-0-dev

# for binary
linux:~ # git clone https://github.com/stlink-org/stlink
linux:~ # cd stlink
linux:~/stlink # cmake .
linux:~/stlink # make
linux:~/stlink # cp ./bin/st-* /usr/local/bin/.
linux:~/stlink # cp ./lib/*.so* /usr/local/lib/.
linux:~/stlink # cp ./config/udev/rules.d/49-stlinkv* /etc/udev/rules.d/.
```

```bash
linux:~ # st-info --version
linux:~ # st-info --probe
linux:~ # st-info --serial

linux:~ # st-flash write <fw>.bin 0x8000000       # write flash
linux:~ # st-flash read <fw>.bin 0x8000000 4096   # read flash
linux:~ # st-flash erase                          # erase flash
```
