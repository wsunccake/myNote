# Sikuli Script

## Install

### Windows

1. 下載 [sikulixset](https://launchpad.net/sikuli/sikulix/1.1.1/+download/sikulixsetup-1.1.1.jar)

2. 點兩下安裝, 1 或 2 至少要勾選一個

![Install](http://sikulix.com/quickstart/files/pasted-graphic.jpg)

### MacOSX

1. 同 windows

2. 因為安全性問題, 需要額外注意安裝

![Mac Install 01](./sikuli/sikuli_mac_01.png)

![Mac Install 02](./sikuli/sikuli_mac_02.png)

### Linux

```
# 編譯時, 使用到的 library
centos:~ # yum install redhat-lsb-core
centos:~ # yum install opencv-core opencv
centos:~ # yum install tesseract

# 執行時, 使用到的 command
centos:~ # yum install wmctrl
centos:~ # yum install xdotool

# install
centos:~ # java -jar sikulisetup-1.1.1.jar
```


## Test

```
centos:~ # tree ex.sikuli
.
├── 1498898231707.png
└── abc.py

centos:~ # cat ex.sikuli/ex.py
openApp('/usr/bin/firefox http://www.google.com')
wait("1498898231707.png", 60)
closeApp('firefox')
```


## Run

### Run as IDE

```
# method 1
centos:~ # runsikulix

# method 2
centos:~ # java -Xmx512M -Dfile.encoding=UTF-8 -Dsikuli.FromCommandLine -jar sikulix.jar
```


### Run as Command

```
# method 1
centos:~ # ./runsikulix -r ex.sikuli

# method 2
centos:~ # java -Xmx512M -Dfile.encoding=UTF-8 -Dsikuli.FromCommandLine -jar sikulix.jar -r ex.sikuli
```


## Reference

[Sikuli Script](http://www.sikuli.org)

[SikuliX](http://sikulix.com/)
