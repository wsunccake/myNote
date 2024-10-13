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

### android sdk tool

[setup android sdk tool](./android_sdk.md)

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

