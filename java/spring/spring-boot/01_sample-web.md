# Spring Boot - Sample Web


## Maven


### Install maven

```
linux:~ # wget http://ftp.tc.edu.tw/pub/Apache/maven/maven-3/3.3.9/binaries/apache-maven-3.3.9-bin.tar.gz
linux:~ # tar zxf apache-maven-3.3.9-bin.tar.gz -C /opt
linux:~ # ln -s /opt/apache-maven-3.3.9 /opt/apache-maven

linux:~ # export MAVEN_HOME=/opt/apache-maven
linux:~ # export PATH=$PATH:$MAVEN_HOME/bin

linux:~ # echo $JAVA_HOME
linux:~ # mvn -v

linux:~ # export MAVEN_OPTS="-Xms512m"
```


### Create project

```
linux:~ # mvn archetype:generate -DgroupId=mypkg -DartifactId=hello -DinteractiveMode=false
linux:~ # cd hello
```


### Write code

```
linux:~/hello # cat pom.xml
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/maven-v4_0_0.xsd">
  <modelVersion>4.0.0</modelVersion>
  <groupId>mypkg</groupId>
  <artifactId>hello</artifactId>
  <packaging>jar</packaging>
  <version>1.0-SNAPSHOT</version>
  <name>hello</name>
  <url>http://maven.apache.org</url>

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>1.5.4.RELEASE</version>
    </parent>
    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
    </dependencies>

    <properties>
        <java.version>1.8</java.version>
    </properties>

    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
                <version>1.5.4.RELEASE</version>
                <executions>
                    <execution>
                        <goals>
                            <goal>repackage</goal>
                        </goals>
                    </execution>
                </executions>
            </plugin>
        </plugins>
    </build>

</project>


linux:~/hello # cat src/main/java/mypkg/SampleController.java
package mypkg;

import org.springframework.boot.*;
import org.springframework.boot.autoconfigure.*;
import org.springframework.stereotype.*;
import org.springframework.web.bind.annotation.*;

@Controller
@EnableAutoConfiguration
public class SampleController {

    @RequestMapping("/")
    @ResponseBody
    String home() {
        return "Hello Spring Boot!";
    }

    public static void main(String[] args) throws Exception {
        SpringApplication.run(SampleController.class, args);
    }
}

linux:~/hello # rm src/main/java/mypkg/App.java 
linux:~/hello # rm src/test/java/mypkg/AppTest.java
```


### Run web

```
# method 1
linux:~/hello # mvn dependency:tree
linux:~/hello # mvn package
linux:~/hello # mvn spring-boot:run

# method 2
linux:~/hello # mvn package spring-boot:repackage
linux:~/hello # java -jar target/hello-1.0-SNAPSHOT.jar
```

http://localhost:8080


## Gradle


### Install gradle

```
# install sdk
linux:~ # curl -s get.sdkman.io | bash
linux:~ # cat ~/.bashrc
source "$HOME/.sdkman/bin/sdkman-init.sh"

# install gradle
linux:~ # sdk list
linux:~ # sdk install gradle
linux:~ # echo $GROOVY_HOME  
```


### Create project

```
linux:~ # mkdir hello
linux:~ # cd hello
linux:~/hello # gradle init
```


### Write code

```
linux:~/hello # cat build.gradle
apply plugin: 'java'
apply plugin: 'org.springframework.boot'

jar {
    baseName = 'hello'
    version =  '0.1.0'
}

repositories {
    mavenCentral()
}

dependencies {
    compile("org.springframework.boot:spring-boot-starter-web:1.5.4.RELEASE")
}

buildscript {
    repositories {
        mavenCentral()
    }
    dependencies {
        classpath("org.springframework.boot:spring-boot-gradle-plugin:1.5.4.RELEASE")
    }
}

linux:~/hello # mkdir -p src/main/java/mypkg
linux:~/hello # cat src/main/java/mypkg/SampleController.java
package mypkg;

import org.springframework.boot.*;
import org.springframework.boot.autoconfigure.*;
import org.springframework.stereotype.*;
import org.springframework.web.bind.annotation.*;

@Controller
@EnableAutoConfiguration
public class SampleController {

    @RequestMapping("/")
    @ResponseBody
    String home() {
        return "Hello Spring Boot!";
    }

    public static void main(String[] args) throws Exception {
        SpringApplication.run(SampleController.class, args);
    }
}
```

### Run web

```
# method 1
linux:~/hello # gradel bootRun

# method 2
linux:~/hello # gradle build
linux:~/hello # java -jar build/libs/hello-0.1.0.jar
```

http://localhost:8080


## Groovy


### Install groovy 

```
linux:~ # sdk install groovy
linux:~ # sdk install springboot 1.5.4.RELEASE
```


### Write code

```
linux:~ # mkdir hello
linux:~ # cd hello
linux:~/hello # cat hello.groovy 
@RestController
class hello {
    @RequestMapping("/")
    String home() {
        "Hello Spring Boot!"
    }
}
```


### Run web

```
linux:~/hello # spring run hello.groovy
```

http://localhost:8080