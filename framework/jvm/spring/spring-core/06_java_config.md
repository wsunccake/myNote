# Java Config

## Hello

`project`

```bash
linux:~/project # gradle init
```

`gradle`

```bash
linux:~/project # vi build.gradle
plugins {
    id 'java'
    id 'application'
}

ext {
    springVersion = "4.1.6.RELEASE"
}

jar {
    baseName = 'spring-project'
    version =  '1.0.0-SNAPSHOT'
}

mainClassName = 'com.mycls.MainApp'

dependencies {
    compile "org.springframework:spring-context:${springVersion}"
}

repositories {
    jcenter()
}
```

`class`

```bash
linux:~/project # vi src/main/java/com/mycls/HelloWorld.java 
package com.mycls;

public class HelloWorld {
   private String message;

   public void setMessage(String message){
      this.message  = message;
   }
   public void getMessage(){
      System.out.println("Your Message : " + message);
   }
}
```

`config`

```bash
linux:~/project # vi src/main/java/com/mycls/HelloWorldConfig.java
package com.mycls;

import org.springframework.context.annotation.*;

@Configuration
public class HelloWorldConfig {
  @Bean 
  public HelloWorld helloWorld(){
    return new HelloWorld();
  }
}
```

@Configuration 設定 class 為 spring java config

@Bean 宣告 method 為 bean

`main class`

```bash
linux:~/project # vi src/main/java/com/mycls/MainApp.java 
package com.mycls;

import org.springframework.context.ApplicationContext;
import org.springframework.context.annotation.*;

public class MainApp {
  public static void main(String[] args) {
    ApplicationContext ctx = 
    new AnnotationConfigApplicationContext(HelloWorldConfig.class);
    HelloWorld helloWorld = ctx.getBean(HelloWorld.class);
    helloWorld.setMessage("Hello World!");
    helloWorld.getMessage();
  }
}
```


---

## Bean

### Scope

`config`

```bash
linux:~/project # vi src/main/java/com/mycls/HelloWorldConfig.java
package com.mycls;

import org.springframework.context.annotation.*;

@Configuration
public class HelloWorldConfig {
  @Bean
  @Scope("prototype")
  public HelloWorld helloWorld(){
    return new HelloWorld();
  }
}
```

@Scope 可以為 singleton 或 prototype


### Life Cycle


### Post Processor


### Definition Inheritance