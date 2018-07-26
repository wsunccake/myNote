# IoC Inversion of Control

## BeanFactory Container

同 01_hello.md 裡的範例, 只是修改 main class

`main class`

```bash
linux:~/spring-project:~ $ vi src/main/java/com/mycls/MainApp.java
package com.mycls;

import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

public class MainApp {
  public static void main(String[] args) {
    XmlBeanFactory factory = new XmlBeanFactory(new ClassPathResource("Beans.xml")); 
    HelloWorld obj = (HelloWorld) factory.getBean("helloWorld");
    obj.getMessage();
  }
}
```

## ApplicationContext Container

同 01_hello.md 裡的範例, 只是修改 main class

`main class`

```bash
linux:~/spring-project:~ $ vi src/main/java/com/mycls/MainApp.java
package com.mycls;

import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

public class MainApp {
  public static void main(String[] args) {
    ApplicationContext context = new FileSystemXmlApplicationContext("~/project/src/Beans.xml");
    HelloWorld obj = (HelloWorld) context.getBean("helloWorld");
    obj.getMessage();
  }
}
```
