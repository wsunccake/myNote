# 簡介

![Gradle](https://en.wikipedia.org/wiki/Gradle#/media/File:Gradle_logo.png)


# install


## with package manager

```bash
# install sdk
[linux:~ ] $ curl -s get.sdkman.io | bash
[linux:~ ] $ cat ~/.bashrc
source "$HOME/.sdkman/bin/sdkman-init.sh"

# install gradle
[linux:~ ] $ sdk list
[linux:~ ] $ sdk install gradle
[linux:~ ] $ echo $GROOVY_HOME         # 確認 Groovy 環境變數

# test
[linux:~ ] $ cat build.gradle
task hello {
    println "Hello"
}
[linux:~ ] $ gradle -q hello
```


## with binary

```bash
[linux:~ ] # mkdir /opt/gradle
[linux:~ ] # unzip -d /opt/gradle gradle-6.8-bin.zip
[linux:~ ] # ls /opt/gradle/gradle-6.8
[linux:~ ] # ln -s /opt/gradle/gradle-6.8/bin/gradle /usr/local/bin/gradle
```


---

# example

Gradle 預設的 build file 名稱為 build.gradle 

```bash
[linux:~ ] $ cat build.gradle
task compile << {
    println 'compiling source'
}

task compileTest(dependsOn: compile) << {
    println 'compiling unit tests'
}

task test(dependsOn: [compile, compileTest]) << {
    println 'running unit tests'
}

task dist(dependsOn: [compile, test]) << {
    println 'building the distribution'
}

# compile
[linux:~ ] $ gradle compile

# dist
[linux:~ ] $ gradle dist

# dist not test
[linux:~ ] $ gradle dist -x test

# compileTest (cT)
[linux:~ ] $ gradle cT

# dist (di)
[linux:~ ] $ gradle di
```


Gradle 可用 -b 指定 build file

```bash
[linux:~ ] $ cat subdir/myproject.gradle
task hello << {
    println "using build file '$buildFile.name' in '$buildFile.parentFile.name'."
}

# 指定特定檔案
[linux:~ ] $ gradle -b subdir/myproject.gradle hello
```


Gradle 可用 -p 指定 build folder

```bash
[linux:~ ] $ cat subdir/build.gradle
task hello << {
    println "using build file '$buildFile.name' in '$buildFile.parentFile.name'."
}

# 指定特定資料夾
[linux:~ ] $ gradle -p subdir hello
```

```bash
[linux:~ ] $ gradle projects

[linux:~ ] $ gradle tasks

# help
[linux:~ ] $ gradle help
[linux:~ ] $ gradle tasks
[linux:~ ] $ gradle tasks --all
[linux:~ ] $ gradle help --task init
```


---

# Java on Gradle

![java_lifecycle](https://docs.gradle.org/current/userguide/img/javaPluginTasks.png)

## folder

```bash
[linux:~/project ] $ mkdir -p src/{main,test}/{java,resources}
[linux:~/project ] $ mkdir -p src/main/{java,test}/mypackage
```


## code

```bash
[linux:~/project ] $ vi src/main/java/mypackage/Hello.java
package mypackage;

import org.apache.log4j.Logger;

public class Hello {
    static Logger logger = Logger.getLogger(Hello.class);

    public static void main(String[] args) {
        String h = new Hello().say();
        if (logger.isDebugEnabled())
            logger.debug("This is debug : " + h);
        if (logger.isInfoEnabled())
            logger.info("This is info : " + h);
        logger.warn("This is warn : " + h);
        logger.error("This is error : " + h);
        logger.fatal("This is fatal : " + h);
    }

    String say() {
        return "Hello Gradle";
    }
}
```


## unit test

```bash
[linux:~/project ] $ vi src/test/java/mypackage/HelloTest.java
package mypackage;

import org.junit.Test;
import static org.junit.Assert.assertEquals;

public class HelloTest {
    @Test
    public void test_hello() {
        assertEquals("Hello Maven", new Hello().say());
    }
}
```


## log4j config

```bash
[linux:~/project ] $ vi src/main/resources/log4j.properties
# Define the root logger with appender file
log = /tmp/log4j
log4j.rootLogger = DEBUG, FILE

# Define the file appender
log4j.appender.FILE=org.apache.log4j.FileAppender
log4j.appender.FILE.File=${log}/log.out

# Define the layout for file appender
log4j.appender.FILE.layout=org.apache.log4j.PatternLayout
log4j.appender.FILE.layout.conversionPattern=%m%n
```


## build file

```bash
[linux:~/project ] $ vi build.gradle
group 'mypackage'
version '1.0-SNAPSHOT'

apply plugin: 'java'

repositories {
    mavenCentral()
}

dependencies {
    compile 'log4j:log4j:1.2.12'
    testCompile 'junit:junit:4.12'
}

task execute(type:JavaExec) {
   main = 'mypackage.Hello'
   classpath = sourceSets.main.runtimeClasspath
}
```


## command

### run with parameter

```bash
# gradle lifecycle command
[linux:~/project ] $ gradle compile  
[linux:~/project ] $ gradle test
[linux:~/project ] $ gradle jar
[linux:~/project ] $ gradle execute

# 若將 build.gradle 中 main = 'mypackage.Hello' 改寫成 main = mainClass (動態載入)
[linux:~/project ] $ gradle -PmainClass=mypackage.Hello execute
```


### run with plugin

```bash
# 另一種方式, 使用 application plugin
[linux:~/project ] $ vi build.gradle
group 'mypackage'
version '1.0-SNAPSHOT'

apply plugin: 'java'
apply plugin: 'application'

mainClassName = 'mypackage.Hello'

repositories {
    mavenCentral()
}

dependencies {
    compile 'log4j:log4j:1.2.12'
    testCompile 'junit:junit:4.12'
}

[linux:~/project ] $ gradle run

# 若將 build.gradle 中 mainClassName = 'mypackage.Hello' 改寫成 main = mainClass (動態載入)
[linux:~/project ] $ gradle -PmainClass=mypackage.Hello run
```


---

# Groovy on Gradle

![grvooy_lifecycle](https://docs.gradle.org/current/userguide/img/groovyPluginTasks.png)


## folder

```bash
[linux:~/project ] $ mkdir -p src/{main,test}/{groovy,resources}
[linux:~/project ] $ mkdir -p src/main/{groovy,test}/mypackage
```


## code

```bash
[linux:~/project ] $ vi src/main/groovy/mypackage/Hello.groovy
package mypackage

import org.apache.log4j.Logger

class Hello {
    static Logger logger = Logger.getLogger(Hello.class)

    static void main(String[] args) {

        String h = new Hello().say()
        if (logger.isDebugEnabled())
            logger.debug("This is debug : " + h)
        if (logger.isInfoEnabled())
            logger.info("This is info : " + h)
        logger.warn("This is warn : " + h)
        logger.error("This is error : " + h)
        logger.fatal("This is fatal : " + h)
    }

    String say() {
        return "Hello Gradle"
    }
}

[linux:~/project ] $ vi src/main/groovy/mypackage/Hello.groovy
package mypackage

println("hi gradle")
```


## unit test

```bash
[linux:~/project ] $ vi src/test/groovy/mypackage/HelloTest.groovy
package mypackage

import org.junit.Test
import static org.junit.Assert.assertEquals

class HelloTest {
    @Test
    void test_hello() {
        assertEquals("Hello Gradle", new Hello().say())
    }
}
```


## log4j config

```bash
[linux:~/project ] $ vi src/main/resources/log4j.properties
# Define the root logger with appender file
log = /tmp/log4j
log4j.rootLogger = DEBUG, FILE

# Define the file appender
log4j.appender.FILE=org.apache.log4j.FileAppender
log4j.appender.FILE.File=${log}/log.out

# Define the layout for file appender
log4j.appender.FILE.layout=org.apache.log4j.PatternLayout
log4j.appender.FILE.layout.conversionPattern=%m%n
```


## build file

```bash
[linux:~/project ] $ vi build.gradle
group 'mypackage'
version '1.0-SNAPSHOT'

apply plugin: 'groovy'
apply plugin: 'application'

repositories {
    mavenCentral()
}

dependencies {
//    compile localGroovy()
    compile 'org.codehaus.groovy:groovy-all:2.4.21'
    compile 'log4j:log4j:1.2.12'
    testCompile 'junit:junit:4.12'
}

task execute(type:JavaExec) {
   main = 'mypackage.Hello'
   classpath = sourceSets.main.runtimeClasspath
}

defaultTasks 'execute'

application {
    mainClass = 'mypackage.hi'
}
```


## command

```bash
[linux:~/project ] $ gradle execute   # task execute
[linux:~/project ] $ gradle -q        # defaultTasks
[linux:~/project ] $ gradle test

[linux:~/project ] $ gradle run       # application
```


---

# init project

```bash
[linux:~/project] $ gradle --help
[linux:~/project] $ gradle help --task init

# create project
[linux:~/project] $ gradle init --type basic --dsl groovy --project-name <project>
[linux:~/project] $ tree
.
├── build.gradle
├── gradle
│   └── wrapper
│       ├── gradle-wrapper.jar
│       └── gradle-wrapper.properties
├── gradlew
├── gradlew.bat
└── settings.gradle

# clean wrapper
[linux:~/project] $ rm -rf gradle gradlew gradlew.bat

# create wrapper
[linux:~/project] $ gradle wrapper
[linux:~/project] $ tree
.
├── build.gradle
├── gradle
│   └── wrapper
│       ├── gradle-wrapper.jar
│       └── gradle-wrapper.properties
├── gradlew
├── gradlew.bat
└── settings.gradle

# list task
[linux:~/project] $ gradle tasks
[linux:~/project] $ ./gradlew tasks
```
