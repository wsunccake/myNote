# arduino develop environment

## usb permit

```bash
linux:~ # usermod -aG dialout <user>
```

## arduino ide

```
File \ Examples \ 01.Basics \ Blink

Sketch \ Verify / Compile
Sketch \ Upload
```

## arduino cli

```bash
linux:~ $ curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | [BINDIR=~/local/bin] sh
```

```bash
linux:~ $ arduino-cli version

linux:~ $ arduino-cli config init               # config -> $HOME/.arduino15\arduino-cli.yaml

linux:~ $ arduino-cli core update-index         # download -> $HOME/.arduino15$ ls staging/packages
linux:~ $ arduino-cli core search               # list all available platform
linux:~ $ arduino-cli core install arduino:avr  # arduino uno
linux:~ $ arduino-cli core show arduino:avr
linux:~ $ arduino-cli core list

linux:~ $ arduino-cli board list
```

```bash
linux:~ $ arduino-cli sketch new blink

linux:~ $ vi blink/blink.ino

linux:~ $ arduino-cli compile --fqbn arduino:avr:uno blink                      # build
linux:~ $ arduino-cli upload -p /dev/ttyUSB<x> --fqbn arduino:avr:uno blink     # upload
linux:~ $ arduino-cli monitor -p /dev/ttyUSB<x> -c baudrate=115200              # monitor charcter
```

```c
// blink/blink.ino
void setup() {
    pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
    digitalWrite(LED_BUILTIN, HIGH);
    delay(500);
    digitalWrite(LED_BUILTIN, LOW);
    delay(500);
}
```

## platformio

```bash
linux:~ $ pip install platformio
linux:~ $ pio --version
linux:~ $ pio system info

linux:~ $ mkdir blink
linux:~ $ cd blink
linux:~/blink $ pio project init --board uno
linux:~/blink $ vi src/main.cpp
linux:~/blink $ pio run                                                 # build -> .pio/build/uno/firmware.hex
linux:~/blink $ pio run --target upload --upload-port /dev/ttyUSB<x>    # upload
linux:~/blink $ pio device monitor --baud 115200 --port /dev/ttyUSB<x>  # monitor
```

```cpp
// src/main.cpp
#include <Arduino.h>

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  digitalWrite(LED_BUILTIN, HIGH);
  delay(1000);
  digitalWrite(LED_BUILTIN, LOW);
  delay(1000);
}
```
