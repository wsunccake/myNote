# linux develop environment

## GNU Arm Embedded Toolchain

[GNU Arm Embedded Toolchain](https://developer.arm.com/downloads/-/gnu-rm)

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

---

## STM32CubeMX

[STM32CubeMX](https://www.st.com/en/development-tools/stm32cubemx.html)

```bash
# prepare
linux:~ # apt install openjdk-11-jdk openjdk-11-jdk-headless

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

---

## STM32CubeProgrammer

[STM32CubeProgrammer](https://www.st.com/en/development-tools/stm32cubeprog.html)

```bash
# for system
linux:~ # unzip en.stm32cubeprg-lin-v2-15-0.zip
linux:~ # ./SetupSTM32CubeProgrammer-2.15.0.linux
linux:~ # /usr/local/STMicroelectronics/STM32Cube/STM32CubeProgrammer/bin/STM32_Programmer_CLI
linux:~ # ln -s /usr/local/STMicroelectronics/STM32Cube/STM32CubeProgrammer/bin/STM32_Programmer_CLI /usr/local/bin/.

# for user
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
linux:~ # STM32_Programmer_CLI -l

linux:~ # STM32_Programmer_CLI -c port=SWD -r32 0x08000000 0x400            # read flash
linux:~ # STM32_Programmer_CLI -c port=SWD -d <fw>.bin 0x08000000 -v   # write flash
linux:~ # STM32_Programmer_CLI -c port=SWD -e all                           # erase flash

linux:~ # STM32_Programmer_CLI -c port=SWD -hardRst                         # hardware reset
linux:~ # STM32_Programmer_CLI -c port=SWD -rst                             # reset
linux:~ # STM32_Programmer_CLI -c port=SWD -s                               # start
```

---

## OpenOCD

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

---

## stlink

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

---

## vscode

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
