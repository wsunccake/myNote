# Android With Gradle


## android sdk tool

[setup android sdk tool](./android_sdk.md)


---

## create project

```bash
centos:~ # mkdir helloAndroid
centos:~ # cd helloAndroid
centos:~/helloAndroid # gradle init
centos:~/helloAndroid # gradle init --type basic --dsl groovy --project-name androidHello
```


---

## gradle config

```bash
centos:~/helloAndroid # vi settings.gradle
rootProject.name = 'helloAndroid'
include ':app'


centos:~/helloAndroid # vi build.gradle
buildscript {
    repositories {
        google()
        jcenter()
        
    }
    dependencies {
        classpath 'com.android.tools.build:gradle:3.4.2'
    }
}

allprojects {
    repositories {
        google()
        jcenter()
        
    }
}

task clean(type: Delete) {
    delete rootProject.buildDir
}
```


---

## create app

```bash
centos:~/helloAndroid # mkdir app
```


---

## app gradle

```bash
centos:~/helloAndroid # vi app/build.gradle
apply plugin: 'com.android.application'

android {
    compileSdkVersion 29
    buildToolsVersion "29.0.1"
    defaultConfig {
        applicationId "com.example.androidhello"
        minSdkVersion 21
        targetSdkVersion 29
        versionCode 1
        versionName "1.0"
    }
    buildTypes {
        release {
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }
}

dependencies {
    implementation fileTree(dir: 'libs', include: ['*.jar'])
    implementation 'androidx.appcompat:appcompat:1.0.2'
    implementation 'androidx.constraintlayout:constraintlayout:1.1.3'
}
```


---

## code

```bash
# mainifest
centos:~/helloAndroid # mkdir -p app/src/main
centos:~/helloAndroid # vi app/src/main/AndroidManifest.xml
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.example.androidhello">

    <application
        android:label="@string/app_name"
        android:theme="@style/AppTheme">

        <activity android:name=".MainActivity">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>

</manifest>


# theme
centos:~/helloAndroid # mkdir -p app/src/main/res/values
centos:~/helloAndroid # app/src/main/res/values/styles.xml
<resources>

    <!-- Base application theme. -->
    <style name="AppTheme" parent="Theme.AppCompat.Light.NoActionBar">
        <!-- Customize your theme here. -->
    </style>

</resources>


# string
centos:~/helloAndroid # mkdir -p app/src/main/res/values
centos:~/helloAndroid # vi app/src/main/res/values/strings.xml
<resources>
    <string name="app_name">androidHello</string>
</resources>


# layout
centos:~/helloAndroid # mkdir -p app/src/main/res/layout
centos:~/helloAndroid # vi app/src/main/res/layout/activity_main.xml
<?xml version="1.0" encoding="utf-8"?>
<android.support.constraint.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity">

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Hello World!"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintLeft_toLeftOf="parent"
        app:layout_constraintRight_toRightOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

</android.support.constraint.ConstraintLayout>


# main
centos:~/helloAndroid # mkdir -p app/src/main/java/com/example/androidhello
centos:~/helloAndroid # vi app/src/main/java/com/example/androidhello/MainActivity.java
package com.example.androidhello;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }
}


# list
centos:~/helloAndroid # tree
centos:~/helloAndroid # ls -R | grep ":$" | sed -e 's/:$//' -e 's/[^-][^\/]*\//--/g' -e 's/^/   /' -e 's/-/|/'
centos:~/helloAndroid # find . | sed -e 's/[^-][^\/]*\//--/g' -e 's/^/   /' -e 's/-/|/' 
```


---

## build

```bash
centos:~/helloAndroid # gradlew build
centos:~/helloAndroid # gradlew installDebug
```


---

## package

connect android phone or emulator first

```bash
# upload apk to remote and install, for developer
centos:~/helloAndroid # adb install app/build/outputs/apk/debug/app-debug.apk
centos:~/helloAndroid # adb uninstall com.example.androidhello

# install on local, for user
centos:~/helloAndroid # adb shell pm install app/build/outputs/apk/debug/app-debug.apk
centos:~/helloAndroid # adb shell pm list packages
centos:~/helloAndroid # adb shell pm list packages com.example.androidhello
centos:~/helloAndroid # adb shell pm uninstall com.example.androidhello
```


---

## test

```
centos:~/helloAndroid # adb shell am start -n com.example.androidhello/.MainActivity
centos:~/helloAndroid # adb shell am force-stop com.example.androidhello
centos:~/helloAndroid # adb shell dumpsys
```


---

## other

```bash
centos:~/helloAndroid # adb shell ps | grep com.example.androidhello
centos:~/helloAndroid # adb shell ps | awk /com.example.androidhello/'{print $2}'
```


---

## ref

[Create a Basic Android App without an IDE](https://developer.okta.com/blog/2018/08/10/basic-android-without-an-ide)
