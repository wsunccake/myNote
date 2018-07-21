# Spring MVC

```
linux:~ # mkdir ex1
linux:~ # cd ex1
linux:~/ex1 # gradle init

linux:~/ex1 # vi build.gradle
apply plugin: 'java'
apply plugin: 'war'
apply plugin: 'eclipse'
apply plugin: 'idea'
apply plugin: 'org.springframework.boot'

jar {
    baseName = 'gs-serving-web-content'
    version =  '0.1.0'
}

repositories {
    mavenCentral()
}

sourceCompatibility = 1.8
targetCompatibility = 1.8

dependencies {
    compile("org.springframework.boot:spring-boot-starter-thymeleaf")
    compile("org.springframework.boot:spring-boot-devtools")
    testCompile("junit:junit")
}

war {
    baseName = 'gs-serving-web-content'
    version = '0.1.0'
}

buildscript {
    repositories {
        mavenCentral()
    }
    dependencies {
        classpath("org.springframework.boot:spring-boot-gradle-plugin:1.5.2.RELEASE")
    }
}


linux:~/ex1 # mkdir -p src/main/java/hello
linux:~/ex1 # vi src/main/java/hello/GreetingController.java
package hello;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;

@Controller
public class GreetingController {

    @RequestMapping("/greeting")
    public String greeting(@RequestParam(value="name", required=false, defaultValue="World") String name, Model model) {
        model.addAttribute("name", name);
        return "greeting";
    }

}

linux:~/ex1 # mkdir -p src/main/resources/templates
linux:~/hello # vi src/main/resources/templates/greeting.html
<!DOCTYPE HTML>
<html xmlns:th="http://www.thymeleaf.org">
<head>
    <title>Getting Started: Serving Web Content</title>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
</head>
<body>
    <p th:text="'Hello, ' + ${name} + '!'" />
</body>
</html>

linux:~/hello # vi src/main/java/hello/Application.java
package hello;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class Application {

    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }

}

linux:~/ex1 # mkdir -p src/main/resources/static
linux:~/ex1 # vi src/main/resources/static/index.html
<!DOCTYPE HTML>
<html>
<head>
    <title>Getting Started: Serving Web Content</title>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
</head>
<body>
    <p>Get your greeting <a href="/greeting">here</a></p>
</body>
</html>


# 使用 gradle 執行
linux:~/ex1 # gradle bootRun

# 使用 gradlew 執行
linux:~/ex1 # ./gradlew bootRun


# 使用 gradle 建立 jar
linux:~/ex1 # gradle build

# 使用 gradlew 建立 jar
linux:~/hello # ./gradlew build

# 執行 jar
linux:~/ex1 # java -jar build/libs/gs-serving-web-content-0.1.0.jar


# 使用 gradle 建立 war
linux:~/ex1 # gradle war

```

http://localhost:8080
http://localhost:8080/greeting
http://localhost:8080/greeting?name=user

