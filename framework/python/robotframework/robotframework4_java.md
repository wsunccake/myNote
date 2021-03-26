# robotframework 4.x


## tool

- openjdk 1.8

- gradle 6.8

- maven 3.6


---

## command - java

download robotframework jar file

```bash
linux:~/project $ vi test.robot
*** Test Cases ***
Test
  Log  Hi Robot Framework

linux:~/project $ java -jar robotframework-4.0.jar test.robot
```


---

## build tool - maven

### demo

```bash
linux:~/project $ vi pom.xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>org.example</groupId>
    <artifactId>project</artifactId>
    <version>1.0-SNAPSHOT</version>

    <properties>
        <maven.compiler.source>1.8</maven.compiler.source>
        <maven.compiler.target>1.8</maven.compiler.target>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.robotframework</groupId>
            <artifactId>robotframework</artifactId>
            <version>4.0</version>
        </dependency>
        <dependency>
            <groupId>org.robotframework</groupId>
            <artifactId>robotframework-maven-plugin</artifactId>
            <version>1.8.0</version>
            <type>maven-plugin</type>
        </dependency>
    </dependencies>


    <build>
        <plugins>
            <plugin>
                <groupId>org.robotframework</groupId>
                <artifactId>robotframework-maven-plugin</artifactId>
                <version>1.8.0</version>
                <executions>
                    <execution>
                        <goals>
                            <goal>run</goal>
                        </goals>
                    </execution>
                </executions>
                <dependencies>
                    <dependency>
                        <groupId>org.robotframework</groupId>
                        <artifactId>robotframework</artifactId>
                        <version>4.0</version>
                    </dependency>
                </dependencies>
            </plugin>
        </plugins>
    </build>

</project>

linux:~/project $ mkdir -p src/test/robotframework/acceptance
linux:~/project $ vi src/test/robotframework/acceptance/test.robot
*** Test Cases ***
Test
  Log  Hi Robot Framework

linux:~/project $ mvn install
linux:~/project $ mvn robotframework:run
```


### import java class

```bash
linux:~/project $ mkdir -p src/main/java/org/example
linux:~/project $ java src/main/java/org/example/MySay.java
package org.example;

public class MySay {

    public String sayHi() {
        return "Hello Robot Framework!";
    }

    public String sayHi(String name) {
        return "Hello " + name;
    }
}

linux:~/project $ vi src/test/robotframework/acceptance/test2.robot
*** Settings ***
Library           org.example.MySay

*** Test Cases ***
Test Java Library
  ${msg1}=  Say Hi
  Log  ${msg1}
  ${msg2}=  Say Hi  robot framework
  Log  ${msg2}

linux:~/project $ mvn install
linux:~/project $ mvn robotframework:run
```


---

## build tool - gradle

### demo

```bash
linux:~/project $ vi settings.gradle
rootProject.name = 'project'

linux:~/project $ vi build.gradle
group 'mypackage'
version '1.0-SNAPSHOT'

apply plugin: 'java'

repositories {
    mavenCentral()
}

dependencies {
    implementation group: 'org.robotframework', name: 'robotframework', version: '4.0'
}

clean{
    delete  'target'
}

task(run, type: JavaExec) {
    main = 'org.robotframework.RobotFramework'
    classpath = sourceSets.main.runtimeClasspath
    args '--variable', 'BROWSER:gc'
    args '--outputdir', 'target'
    args 'src/test/robotframework/acceptance'
}

linux:~/project $ mkdir -p src/test/robotframework/acceptance
linux:~/project $ vi src/test/robotframework/acceptance/test.robot
*** Test Cases ***
Test
  Log  Hi Robot Framework

linux:~/project $ gradle run
```


### import java class

```bash
linux:~/project $ mkdir -p src/main/java/mypackage
linux:~/project $ java src/main/java/mypackage/MySay.java
package mypackage;

public class MySay {

    public String sayHi() {
        return "Hello Robot Framework!";
    }

    public String sayHi(String name) {
        return "Hello " + name;
    }
}

linux:~/project $ vi src/test/robotframework/acceptance/test2.robot
*** Settings ***
Library           mypackage.MySay

*** Test Cases ***
Test Java Library
  ${msg1}=  Say Hi
  Log  ${msg1}
  ${msg2}=  Say Hi  robot framework
  Log  ${msg2}

linux:~/project $ gradle run
```
