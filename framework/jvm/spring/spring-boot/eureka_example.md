# Eurekra


## Eurekra Server

`project`

```bash
linux:~ # mkdir service-registry
linux:~ # cd service-registry
```

`gradle`

```bash
linux:~/service-registry # vi build.gradle
buildscript {
    ext {
        springBootVersion = '2.0.4.RELEASE'
    }
    repositories {
        mavenCentral()
    }
    dependencies {
        classpath("org.springframework.boot:spring-boot-gradle-plugin:${springBootVersion}")
    }
}

apply plugin: 'java'
apply plugin: 'org.springframework.boot'
apply plugin: 'io.spring.dependency-management'

group = 'com.example'
version = '0.0.1-SNAPSHOT'
sourceCompatibility = 1.8

repositories {
    mavenCentral()
}


ext {
    springCloudVersion = 'Finchley.SR1'
}

dependencies {
    compile('org.springframework.cloud:spring-cloud-starter-netflix-eureka-server')
    testCompile('org.springframework.boot:spring-boot-starter-test')
}

dependencyManagement {
    imports {
        mavenBom "org.springframework.cloud:spring-cloud-dependencies:${springCloudVersion}"
    }
}


linux:~/service-registry # vi settings.gradle
rootProject.name = 'service-registry'

linux:~/service-discovery # gradle wrapper --gradle-version 4.9
```

`main`

```bash
linux:~/service-registry # vi src/main/java/com/example/EurekaServiceApplication.java
package com.example;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.netflix.eureka.server.EnableEurekaServer;

@EnableEurekaServer
@SpringBootApplication
public class EurekaServiceApplication {
    public static void main(String[] args) {
        SpringApplication.run(EurekaServiceApplication.class, args);
    }
}
```

`property`

```bash
linux:~/service-registry # vi src/main/resources/application.properties
server.port=${PORT:8761}

eureka.client.register-with-eureka=false
eureka.client.fetch-registry=false

logging.level.com.netflix.eureka=OFF
logging.level.com.netflix.discovery=OFF
```

`run`

```bash
linux:~/service-registry # gradle wrapper
linux:~/service-registry # ./gradlew bootRun
```

`check`

```bash
linux:~ # curl http://localhost:8761/
```


---

## Eureka Clinet - provider

`project`

```bash
linux:~ # mkdir service-provider
linux:~ # cd service-provider
```

`gradle`

```bash
linux:~/service-provider # vi build.gradle
buildscript {
    ext {
        springBootVersion = '2.0.4.RELEASE'
    }
    repositories {
        mavenCentral()
    }
    dependencies {
        classpath("org.springframework.boot:spring-boot-gradle-plugin:${springBootVersion}")
    }
}

apply plugin: 'java'
apply plugin: 'idea'
apply plugin: 'org.springframework.boot'
apply plugin: 'io.spring.dependency-management'

group = 'com.example'
version = '0.0.1-SNAPSHOT'
sourceCompatibility = 1.8

repositories {
    mavenCentral()
}

ext {
    springCloudVersion = 'Finchley.SR1'
}

dependencies {
    compile('org.springframework.boot:spring-boot-starter-web')
    compile('org.springframework.cloud:spring-cloud-starter-netflix-eureka-client')
    testCompile('org.springframework.boot:spring-boot-starter-test')
}

dependencyManagement {
    imports {
        mavenBom "org.springframework.cloud:spring-cloud-dependencies:${springCloudVersion}"
    }
}


linux:~/service-provider # vi settings.gradle
rootProject.name = 'service-provider'

linux:~/service-provider # gradle wrapper
```

`main`

```bash
linux:~/service-provider # vi src/main/java/com/example/ServerApp.java 
package com.example;


import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.netflix.eureka.EnableEurekaClient;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.beans.factory.annotation.Value;


@EnableEurekaClient
@SpringBootApplication
public class ServerApp {
    public static void main(String[] args) {
        SpringApplication.run(ServerApp.class, args);
    }
}


@RestController
class ServerController {
    @Value("${server.port}")
    String port;

    @RequestMapping("/")
    @ResponseBody
    public String home() {
        return String.format("Server port: %s !", port);
    }
}
```

`property`

```bash
linux:~/service-provider # vi src/main/resources/application.yml
server:
  port: 8098

eureka:
  instance:
    leaseRenewalIntervalInSeconds: 1
    leaseExpirationDurationInSeconds: 2
  client:
    serviceUrl:
      defaultZone: http://127.0.0.1:8761/eureka/
    healthcheck:
      enabled: false
    lease:
      duration: 5

spring:
  application:
    name: service-provider

management:
  security:
    enabled: false
```

`run`

```bash
linux:~/service-provider # gradle wrapper
linux:~/service-provider # ./gradlew bootRun
```

`check`

```bash
linux:~ # curl http://localhost:8098/
```

---


## Eureka Clinet - consumer

`project`

```bash
linux:~ # mkdir service-consumer
linux:~ # cd service-consumer
```

`gradle`

```bash
linux:~/service-consumer # vi build.gradle
buildscript {
    ext {
        springBootVersion = '2.0.4.RELEASE'
    }
    repositories {
        mavenCentral()
    }
    dependencies {
        classpath("org.springframework.boot:spring-boot-gradle-plugin:${springBootVersion}")
    }
}

apply plugin: 'java'
apply plugin: 'idea'
apply plugin: 'org.springframework.boot'
apply plugin: 'io.spring.dependency-management'

group = 'com.example'
version = '0.0.1-SNAPSHOT'
sourceCompatibility = 1.8

repositories {
    mavenCentral()
}


ext {
    springCloudVersion = 'Finchley.SR1'
}

dependencies {
    compile('org.springframework.boot:spring-boot-starter-web')
    compile('org.springframework.cloud:spring-cloud-starter-netflix-eureka-client')
    compile('org.springframework.boot:spring-boot-starter-actuator')
    testCompile('org.springframework.boot:spring-boot-starter-test')
}

dependencyManagement {
    imports {
        mavenBom "org.springframework.cloud:spring-cloud-dependencies:${springCloudVersion}"
    }
}


linux:~/service-consumer # vi settings.gradle
rootProject.name = 'service-consumer'

linux:~/service-consumer # gradle wrapper
```

`main`

```bash
linux:~/service-consumer # vi src/main/java/com/example/ClientApp.java 
package com.example;
 
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.client.loadbalancer.LoadBalanced;
import org.springframework.cloud.netflix.eureka.EnableEurekaClient;
import org.springframework.context.annotation.Bean;
import org.springframework.http.HttpMethod;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;

@SpringBootApplication
@EnableEurekaClient
public class ClientApp {
 
    public static void main(String[] args) {
        SpringApplication.run(ClientApp.class, args);
    }
}

@RestController
class ClientController {
    @Autowired
    RestTemplate restTemplate;

    @LoadBalanced
    @Bean
    public RestTemplate restTemplate() {
        return new RestTemplate();
    }

    @RequestMapping(value = "/", method = RequestMethod.GET)
    public String getStudents() {
        String body = restTemplate.getForEntity("http://service-provider", String.class).getBody();
//        String body = restTemplate.exchange("http://service-provider/", HttpMethod.GET, null, String.class).getBody();
        return "Consumer get message: " + body;
    }

}
```

`property`

```bash
linux:~/service-consumer # vi src/main/resources/application.yml
server:
  port: 9098
 
eureka:
  instance:
    leaseRenewalIntervalInSeconds: 1
    leaseExpirationDurationInSeconds: 2
  client:
    serviceUrl:
      defaultZone: http://127.0.0.1:8761/eureka/
    healthcheck:
      enabled: true   # include spring-boot-starter-actuator
    lease:
      duration: 5
 
spring:
  application:
    name: service-cosumer
```

`run`

```bash
linux:~/service-consumer # gradle wrapper
linux:~/service-consumer # ./gradlew bootRun
```

`check`

```bash
linux:~ # curl http://localhost:9098/
```


---

## Ref

[Spring Cloud Service Discovery with Netflix Eureka](https://howtodoinjava.com/spring-cloud/spring-cloud-service-discovery-netflix-eureka/)

[Wind Mt](https://windmt.com/)
