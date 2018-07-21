# Bean

## Scope

同 01_hello.md 裡的範例, 只是改變 bean config 的 scope 設定和修改 main class

`main class`

```bash
linux:~/spring-project:~ $ vi src/main/java/com/mycls/MainApp.java
package com.mycls;

import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

public class MainApp {
  public static void main(String[] args) {
    ApplicationContext context = new ClassPathXmlApplicationContext("Beans.xml");
    HelloWorld objA = (HelloWorld) context.getBean("helloWorld");
    objA.setMessage("I'm object A");
    objA.getMessage();
    HelloWorld objB = (HelloWorld) context.getBean("helloWorld");
    objB.getMessage();
  }
}
```

### singleton

`bean config`

當 scope 為 singleton, obj1 和 obj2 為一樣的 obj

```bash
linux:~/spring-project:~ $ vi src/main/resources/Beans.xml
<beans xmlns="http://www.springframework.org/schema/beans"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://www.springframework.org/schema/beans
  http://www.springframework.org/schema/beans/spring-beans.xsd">
  <bean id="helloBean" class="com.mycls.HelloWorld" scope="singleton">
    <property name="message" value="Hello Spring" />
  </bean>
</beans>
```


### prototype

`bean config`

當 scope 為 prototype, obj1 和 obj2 為不同的 obj

```bash
linux:~/spring-project:~ $ vi src/main/resources/Beans.xml
<beans xmlns="http://www.springframework.org/schema/beans"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://www.springframework.org/schema/beans
  http://www.springframework.org/schema/beans/spring-beans.xsd">
  <bean id="helloBean" class="com.mycls.HelloWorld" scope="prototype">
    <property message="name" value="Hello Spring" />
  </bean>
</beans>
```


---

## Life Cycle

同 01_hello.md 裡的範例, 只是改變 bean config 設定, 修改 main class 以及增加 class 裡面的 method

`class`

新增 init 和 destroy 兩個 method

```bash
linux:~/spring-project $ vi src/main/java/com/mycls/HelloWorld.java
package com.mycls;

public class HelloWorld {
  private String message;

  public void setMessage(String message){
    this.message = message;
  }
  public void getMessage(){
    System.out.println("Your Message : " + message);
  }
  public void init(){
    System.out.println("Bean is going through init.");
  }
  public void destroy() {
    System.out.println("Bean will destroy now.");
  }
}
```

`main class`

context.registerShutdownHook 宣告不使用的 obj 回收

```bash
linux:~/spring-project:~ $ vi src/main/java/com/mycls/MainApp.java
ppackage com.mycls;

import org.springframework.context.support.AbstractApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

public class MainApp {
  public static void main( String[] args ) {
    AbstractApplicationContext context = new ClassPathXmlApplicationContext("Beans.xml");
    HelloWorld obj = (HelloWorld) context.getBean("helloWorld");
    obj.getMessage();
    context.registerShutdownHook();
  }
}
```

`bean config`

init-method hook this class init method

destroy-method hook this class destroy method

```bash
linux:~/spring-project:~ $ vi src/main/resources/Beans.xml
<beans xmlns="http://www.springframework.org/schema/beans"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://www.springframework.org/schema/beans
  http://www.springframework.org/schema/beans/spring-beans.xsd">
<!--   default-init-method = "init"       -->
<!--   default-destroy-method = "destroy" -->
  <bean id="helloBean" class="com.mycls.HelloWorld" init-method="init" destroy-method="destroy">
    <property name="message" value="Hello Spring" />
  </bean>
</beans>
```


---

## Post Processor

同 01_hello.md 裡的範例, 需修改 bean config, main class 以及 class

`class`

```bash
linux:~/spring-project $ vi src/main/java/com/mycls/HelloWorld.java
package com.mycls;

public class HelloWorld {
  private String message;

  public void setMessage(String message){
    this.message  = message;
  }
  public void getMessage(){
    System.out.println("Your Message : " + message);
  }
  public void init(){
    System.out.println("Bean is going through init.");
  }
  public void destroy(){
    System.out.println("Bean will destroy now.");
  }
}
```

```bash
linux:~/spring-project $ vi src/main/java/com/mycls/InitHelloWorld.java
package com.mycls;

import org.springframework.beans.factory.config.BeanPostProcessor;
import org.springframework.beans.BeansException;

public class InitHelloWorld implements BeanPostProcessor {
  public Object postProcessBeforeInitialization(Object bean, String beanName)
    throws BeansException {
      System.out.println("BeforeInitialization : " + beanName);
      return bean;  // you can return any other object as well
  }
  public Object postProcessAfterInitialization(Object bean, String beanName)
    throws BeansException {
      System.out.println("AfterInitialization : " + beanName);
      return bean;  // you can return any other object as well
  }
}
```

`main class`

```bash
linux:~/spring-project:~ $ vi src/main/java/com/mycls/MainApp.java
ppackage com.mycls;

import org.springframework.context.support.AbstractApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

public class App {
  public static void main( String[] args ) {
    AbstractApplicationContext context = new ClassPathXmlApplicationContext("Beans.xml");
    HelloWorld obj = (HelloWorld) context.getBean("helloWorld");
    obj.getMessage();
    context.registerShutdownHook();
    }
}
```

`bean config`

init-method hook this class init method

destroy-method hook this class destroy method

```bash
linux:~/spring-project:~ $ vi src/main/resources/Beans.xml
<beans xmlns="http://www.springframework.org/schema/beans"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://www.springframework.org/schema/beans
  http://www.springframework.org/schema/beans/spring-beans.xsd">
  <bean id="helloBean" class="com.mycls.HelloWorld" init-method="init" destroy-method="destroy">
    <property name="message" value="Hello Spring"/>
  </bean>
  <bean class="com.mycls.InitHelloWorld" />
</beans>
```


---

## Definition Inheritance

同 01_hello.md 裡的範例, 需修改 bean config 以及 class

`class`

```bash
linux:~/spring-project $ vi src/main/java/com/mycls/HelloWorld.java
package com.mycls;

public class HelloWorld {
  private String message1;
  private String message2;

  public void setMessage1(String message){
   this.message1 = message;
  }
  public void setMessage2(String message){
   this.message2 = message;
  }
  public void getMessage1(){
   System.out.println("World Message1 : " + message1);
  }
  public void getMessage2(){
   System.out.println("World Message2 : " + message2);
  }
}
```

`bean config`

```bash
linux:~/spring-project:~ $ vi src/main/resources/Beans.xml
<beans xmlns="http://www.springframework.org/schema/beans"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://www.springframework.org/schema/beans
  http://www.springframework.org/schema/beans/spring-beans.xsd">
    <bean id = "beanTeamplate" abstract = "true">
        <property name="message1" value = "Hell Spring"/>
        <property name="message2" value = "Hi Spring"/>
    </bean>
    <bean id="helloBean" class="com.mycls.HelloWorld" parent="beanTeamplate">
    <property name="message1" value="Good Spring"/>
  </bean>
</beans>
```
