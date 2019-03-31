# Appium


## require


### nodejs

https://nodejs.org/en/download/

```bash
centos:~ # tar Jxf node-v10.15.3-linux-x64.tar.xz -C /opt
centos:~ # export PATH=/opt/node-v10.15.3-linux-x64/bin:$PATH
centos:~ # node -v
```

### chrome

```bash
centos:~ # vi /etc/yum.repos.d/google.repo
[google64]
name=Google - x86_64
baseurl=http://dl.google.com/linux/rpm/stable/x86_64
enabled=1
gpgcheck=1
gpgkey=https://dl-ssl.google.com/linux/linux_signing_key.pub
centos:~ # yum install google-chrome-stable
centos:~ # google-chrome-stable --version
```

### chrome web driver

check version and download

http://chromedriver.chromium.org/downloads, https://chromedriver.storage.googleapis.com/index.html

```bash
centos:~ # unzip chromedriver_linux64.zip -d /usr/local/bin

# check chrome web driver
centos:~ # yum install python36
centos:~ # curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
centos:~ # python36 get-pip.py
centos:~ # pip3 install selenium
centos:~ # selenium_test.py

from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
driver = webdriver.Chrome(chrome_options=options)
driver.get('https://www.google.com')

print(driver.title)

driver.quit()
```

### java

```bash
centos:~ # java-1.8.0-openjdk-devel
centos:~ # export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk
centos:~ # export PATH=$JAVA_HOME/bin:$PATH
```

### android sdk tool

https://developer.android.com/studio

```bash
centos:~ # unzip sdk-tools-linux-4333796.zip -d /opt/android-sdk
centos:~ # export ANDROID_HOME=/opt/android-sdk
centos:~ # export PATH=$ANDROID_HOME/tools:$ANDROID_HOME/tools/bin:$ANDROID_HOME/platform-tools:$PATH
centos:~ # export REPO_OS_OVERRIDE=linux
centos:~ # sdkmanager --licenses
centos:~ # sdkmanager --list
centos:~ # sdkmanager "tools" "platform-tools"
centos:~ # adb --version

# create andoird emulator
export ANDROID_SDK_ROOT=/opt/android-sdk
centos:~ # sdkmanager "build-tools;28.0.0" "system-images;android-28;google_apis;x86_64" "platforms;android-28"
centos:~ # avdmanager list
centos:~ # avdmanager create avd -n test -k "system-images;android-28;google_apis;x86_64"
centos:~ # emulator -list-avds
centos:~ # vi .android/avd/test.avd/config.ini
hw.gpu.enabled=no
hw.gpu.mode=mesa

centos:~ # emulator -adv test
centos:~ # android list target         # get device name
centos:~ # avdmanager delete avd -n
```

sdk folder must exist emulator, platforms, platform-tools, system-images

---

## install


```
centos:~ # npm install -g appium
centos:~ # npm install -g appium-doctor
centos:~ # appium-doctor
```


---

## test

```bash
centos:~ # pip3 install Appium-Python-Client
centos:~ # android_example.py
from appium import webdriver

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '9'
desired_caps['deviceName'] = 'Android Emulator'
desired_caps['appPackage'] = 'com.android.calculator2'
desired_caps['appActivity'] = '.Calculator'

driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
driver.quit()
```

- git clone https://github.com/appium-boneyard/sample-code.git

