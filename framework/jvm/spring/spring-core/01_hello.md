# Hello


## Maven

`project`

使用 maven 建立 project

```bash
linux:~$ mvn archetype:generate -DgroupId=com.mycls -DartifactId=sping-example -DarchetypeArtifactId=maven-archetype-quickstart -DinteractiveMode=false
linux:~ $ cd sping-example
linux:~/spring-example:~ $ tree
.
├── pom.xml
└── src
    ├── main
    │   └── java
    │       └── com
    │           └── mycls
    └── test
        └── java
            └── com
                └── mycls
```

`pom.xml`

將用到的 jar 寫入到 pom.xml

```bash
linux:~/spring-example:~ $ vi pom.xml
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/maven-v4_0_0.xsd">
  <modelVersion>4.0.0</modelVersion>
  <groupId>com.mycls</groupId>
  <artifactId>sping-example</artifactId>
  <packaging>jar</packaging>
  <version>1.0-SNAPSHOT</version>
  <name>sping-example</name>
  <url>http://maven.apache.org</url>

  <properties>
    <spring.version>4.1.6.RELEASE</spring.version>
  </properties>

  <dependencies>
    <dependency>
      <groupId>org.springframework</groupId>
      <artifactId>spring-core</artifactId>
      <version>${spring.version}</version>
    </dependency>

    <dependency>
      <groupId>org.springframework</groupId>
      <artifactId>spring-context</artifactId>
      <version>${spring.version}</version>
    </dependency>

    <dependency>
      <groupId>junit</groupId>
      <artifactId>junit</artifactId>
      <version>3.8.1</version>
      <scope>test</scope>
    </dependency>
  </dependencies>
</project>
```

`class`

```bash
linux:~/spring-example:~ $ vi src/main/java/com/mycls/HelloWorld.java
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

`bean config`

使用 xml 格式設定 bean

```bash
linux:~/spring-example:~ $ mkdir -p src/main/resources
linux:~/spring-example:~ $ src/main/resources/Beans.xml
<beans xmlns="http://www.springframework.org/schema/beans"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://www.springframework.org/schema/beans
  http://www.springframework.org/schema/beans/spring-beans.xsd">
  <bean id="helloBean" class="com.mycls.HelloWorld">
    <property name="message" value="Hello Spring" />
  </bean>
</beans>
```

`main class`

ClassPathXmlApplicationContext 讀取 bean config

context.getBean 將 bean 載入

```bash
linux:~/spring-example:~ $ vi src/main/java/com/mycls/MainApp.java
package com.mycls;

import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

public class MainApp {
  public static void main(String[] args) {
    ApplicationContext context = new ClassPathXmlApplicationContext("Beans.xml");
    HelloWorld obj = (HelloWorld) context.getBean("helloWorld");
    obj.getMessage();
  }
}
```

`execution`

```bash
linux:~/spring-example:~ $ tree
.
├── pom.xml
└── src
    ├── main
    │   ├── java
    │   │   └── com
    │   │       └── mycls
    │   │           └── HelloWorld.java
    │   └── resources
    │       └── SpringBeans.xml
    └── test
        └── java
            └── com
                └── mycls

linux:~/spring-example:~ $ mvn package
linux:~/spring-example:~ $ mvn exec:java -Dexec.mainClass=com.mycls.App
```


---

## Gradle

`project`

使用 gradle 建立 project

```bash
linux:~ $ mkdir spring-project
linux:~ $ cd spring-project
linux:~/spring-project:~ $ gradle init
linux:~/spring-project:~ $ tree 
.
├── build.gradle
├── gradle
│   └── wrapper
│       ├── gradle-wrapper.jar
│       └── gradle-wrapper.properties
├── gradlew
├── gradlew.bat
└── settings.gradle
```

`build.gradle`

將用到的 jar 寫入到 pom.xml

mainClassName 設定 main class 所在位置

```bash
linux:~/spring-project:~ $ vi build.gradle
apply plugin: 'java'
apply plugin: 'application'

//mainClassName = 'com.mycls.App'

jar {
    baseName = 'spring-project'
    version =  '1.0.0-SNAPSHOT'
}

repositories {
    jcenter()
    mavenLocal()
    mavenCentral()
}

dependencies {
    compile("org.springframework:spring-context:${springVersion}")
}

# 將版本抽出來當變數
linux:~/spring-project:~ $ vi gradle.properties 
springVersion=4.1.6.RELEASE
```

`class`

```bash
linux:~/spring-project $ mkdir -p src/main/java/com/mycls
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
}
```

`bean config`

使用 xml 格式設定 bean

```bash
linux:~/spring-project:~ $ mkdir -p src/main/resources
linux:~/spring-project:~ $ vi src/main/resources/Beans.xml
<beans xmlns="http://www.springframework.org/schema/beans"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://www.springframework.org/schema/beans
  http://www.springframework.org/schema/beans/spring-beans.xsd">
  <bean id="helloBean" class="com.mycls.HelloWorld">
    <property name="message" value="Hello Sping" />
  </bean>
</beans>
```

`main class`

ClassPathXmlApplicationContext 讀取 bean config

context.getBean 將 bean 載入

```bash
linux:~/spring-project:~ $ vi src/main/java/com/mycls/MainApp.java
package com.mycls;

import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

public class MainApp {
  public static void main(String[] args) {
    ApplicationContext context = new ClassPathXmlApplicationContext("Beans.xml");
    HelloWorld obj = (HelloWorld) context.getBean("helloWorld");
    obj.getMessage();
  }
}
```

`execution`

-PmainClassName 會 overwrite build.gradle 設定

```bash
linux:~/spring-project:~ $ gradle jar
linux:~/spring-project:~ $ gradle -PmainClass=com.mycls.MainApp run
```


---

## IntelliJ IDEA

