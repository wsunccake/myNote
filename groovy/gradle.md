# 簡介

![Gradle](http://gradle.wpengine.netdna-cdn.com/wp-content/uploads/2015/10/gradle-logo-horizontal2.svg)


# 安裝

```
# install sdk
linux:~ $ curl -s get.sdkman.io | bash
linux:~ $ cat ~/.bashrc
source "$HOME/.sdkman/bin/sdkman-init.sh"

# install gradle
linux:~ $ sdk list
linux:~ $ sdk install gradle
linux:~ $ echo $GROOVY_HOME         # 確認 Groovy 環境變數

# test
linux:~ $ cat build.gradle
task hello {
    println "Hello"
}
linux:~ $ gradle -q hello
```

# 範例

Gradle 預設的 build file 名稱為 build.gradle 

```
linux:~ # cat build.gradle
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

# 執行 compile
linux:~ # gradle compile

# 執行 dist
linux:~ # gradle dist

# 執行 dist 但不執行 test
linux:~ # gradle dist -x test

# 執行 compileTest (縮寫成 cT)
linux:~ # gradle cT

# 執行 dist (縮寫成 di)
linux:~ # gradle di
```


Gradle 可用 -b 指定 build file

```
linux:~ # cat subdir/myproject.gradle
task hello << {
    println "using build file '$buildFile.name' in '$buildFile.parentFile.name'."
}

# 指定特定檔案
linux:~ # gradle -b subdir/myproject.gradle hello
```


Gradle 可用 -p 指定 build folder

```
linux:~ # cat subdir/build.gradle
task hello << {
    println "using build file '$buildFile.name' in '$buildFile.parentFile.name'."
}

# 指定特定資料夾
linux:~ # gradle -p subdir hello
```

```
linux:~ # gradle projects

linux:~ # gradle tasks
```


# Java on Gradle

![java_lifecycle](https://docs.gradle.org/current/userguide/img/javaPluginTasks.png)

```
# folder
linux:~/project # mkdir -p src/{main,test}/{java,resources}
linux:~/project # mkdir -p src/main/{java,test}/mypackage


# code
linux:~/project # vi src/main/java/mypackage/Hello.java
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
        return "Hello Maven";
    }
}


# log4j config
linux:~/project # vi src/main/resources/log4j.properties
# Define the root logger with appender file
log = /tmp/log4j
log4j.rootLogger = DEBUG, FILE

# Define the file appender
log4j.appender.FILE=org.apache.log4j.FileAppender
log4j.appender.FILE.File=${log}/log.out

# Define the layout for file appender
log4j.appender.FILE.layout=org.apache.log4j.PatternLayout
log4j.appender.FILE.layout.conversionPattern=%m%n


# unit test
linux:~/project # vi src/test/java/mypackage/HelloTest.java
package mypackage;

import org.junit.Test;
import static org.junit.Assert.assertEquals;

public class HelloTest {
    @Test
    public void test_hello() {
        assertEquals("Hello Maven", new Hello().say());
    }
}


# build file
linux:~/project # vi build.gradle
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


# gradle lifecycle command
linux:~/project # gradle compile  
linux:~/project # gradle test
linux:~/project # gradle jar
linux:~/project # gradle execute

# 若將 build.gradle 中 main = 'mypackage.Hello' 改寫成 main = mainClass (動態載入)
linux:~/project # gradle -PmainClass=mypackage.Hello execute
```


# Groovy on Gradle

![grvooy_lifecycle](https://docs.gradle.org/current/userguide/img/groovyPluginTasks.png)

```
linux:~ # mkdir -p src/{main,test}/{java,groovy,resources}



apply plugin: 'eclipse'
apply plugin: 'groovy'

repositories {
    mavenCentral()
}

dependencies {
    compile 'org.codehaus.groovy:groovy-all:2.4.4'
    testCompile 'junit:junit:4.12'
}
```