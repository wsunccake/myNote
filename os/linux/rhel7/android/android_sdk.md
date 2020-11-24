# Java

```bash
centos:~ # yum install java-1.8.0-openjdk-devel
centos:~ # export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk
centos:~ # export PATH=$JAVA_HOME/bin:$PATH
centos:~ # java -version
```


---

# Android SDK Tool

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


## sdkmanager

```bash
centos:~ # sdkmanager --licenses
centos:~ # sdkmanager --list
centos:~ # sdkmanager "tools" "platform-tools"
```


## avdmanager

```bash
centos:~ # avdmanager --help
centos:~ # avdmanager list
centos:~ # avdmanager list avd
centos:~ # avdmanager list target
centos:~ # avdmanager list device
centos:~ # avdmanager create avd -n test -k "system-images;android-28;google_apis;x86_64"
centos:~ # avdmanager move avd -n test -r demo
centos:~ # avdmanager delete avd -n test
```


## emulator

```bash
centos:~ # cd $ANDROID_HOME/tools
centos:/opt/android-sdk/tools # emulator -help
centos:/opt/android-sdk/tools # emulator -list-avds
centos:/opt/android-sdk/tools # emulator -avd <avd_name>
```


## adb

```bash
centos:~ # adb
centos:~ # adb devices
centos:~ # adb logcat
centos:~ # adb install <package>.apk
```

---

# Android Studio

https://developer.android.com/studio

