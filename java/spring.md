# 簡介


----

# Create Project


## via Maven

```
Linux:~$ mvn archetype:generate -DgroupId=com.mycls -DartifactId=sping-example -DarchetypeArtifactId=maven-archetype-quickstart -DinteractiveMode=false
Linux:~ $ cd sping-example
Linux:~/spring-example:~ $ tree
.
├── pom.xml
└── src
    ├── main
    │   └── java
    │       └── com
    │           └── mycls
    │               └── App.java
    └── test
        └── java
            └── com
                └── mycls
                    └── AppTest.java

Linux:~/spring-example:~ $ vi pom.xml
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

Linux:~/spring-example:~ $ vi src/main/java/com/mycls/HelloWorld.java
package com.mycls;

public class HelloWorld {
	private String name;

	public void setName(String name) {
		this.name = name;
	}

	public void printHello() {
		System.out.println("Spring: Hello! " + name);
	}
}

Linux:~/spring-example:~ $ mkdir -p src/main/resources
Linux:~/spring-example:~ $ src/main/resources/SpringBeans.xml
<beans xmlns="http://www.springframework.org/schema/beans"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://www.springframework.org/schema/beans
  http://www.springframework.org/schema/beans/spring-beans-3.0.xsd">

<bean id="helloBean" class="com.mycls.HelloWorld">
  <property name="name" value="MMmm" />
  </bean>
</beans>

Linux:~/spring-example:~ $ vi src/main/java/com/mycls/App.java
package com.mycls;

import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

public class App {
	public static void main( String[] args ) {
		ApplicationContext context = new ClassPathXmlApplicationContext("SpringBeans.xml");
		HelloWorld obj = (HelloWorld) context.getBean("helloBean");
		obj.printHello();
	}
}

Linux:~/spring-example:~ $ tree
.
├── pom.xml
└── src
    ├── main
    │   ├── java
    │   │   └── com
    │   │       └── mycls
    │   │           ├── App.java
    │   │           └── HelloWorld.java
    │   └── resources
    │       └── SpringBeans.xml
    └── test
        └── java
            └── com
                └── mycls
                    └── AppTest.java

Linux:~/spring-example:~ $ mvn package
Linux:~/spring-example:~ $ mvn exec:java -Dexec.mainClass=com.mycls.App
```

## via Gradle

```
Linux:~ $ mkdir spring-project
Linux:~ $ cd spring-project
Linux:~/spring-project:~ $ gradle init --type java-library
Linux:~/spring-project:~ $ tree 
.
├── build.gradle
├── gradle
│   └── wrapper
│       ├── gradle-wrapper.jar
│       └── gradle-wrapper.properties
├── gradlew
├── gradlew.bat
├── settings.gradle
└── src
    ├── main
    │   └── java
    │       └── Library.java
    └── test
        └── java
            └── LibraryTest.java

Linux:~/spring-project:~ $ vi build.gradle
apply plugin: 'java'
apply plugin: 'application'

mainClassName = mainClass

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
    compile 'org.slf4j:slf4j-api:1.7.21'
    compile("org.springframework:spring-context:${springVersion}")

    testCompile 'junit:junit:4.12'
}
Linux:~/spring-project:~ $ vi gradle.properties 
springVersion=4.1.6.RELEASE

Linux:~/spring-project $ mkdir -p src/main/java/com/mycls
Linux:~/spring-project $ vi src/main/java/com/mycls/HelloWorld.java
package com.mycls;

public class HelloWorld {
	private String name;

	public void setName(String name) {
		this.name = name;
	}

	public void printHello() {
		System.out.println("Spring: Hello! " + name);
	}
}

Linux:~/spring-project:~ $ mkdir -p src/main/resources
Linux:~/spring-project:~ $ vi src/main/resources/SpringBeans.xml
<beans xmlns="http://www.springframework.org/schema/beans"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://www.springframework.org/schema/beans
  http://www.springframework.org/schema/beans/spring-beans-3.0.xsd">

<bean id="helloBean" class="com.mycls.HelloWorld">
  <property name="name" value="MMmm" />
  </bean>
</beans>

Linux:~/spring-project:~ $ vi src/main/java/com/mycls/App.java
package com.mycls;

import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

public class App {
	public static void main( String[] args ) {
		ApplicationContext context = new ClassPathXmlApplicationContext("SpringBeans.xml");
		HelloWorld obj = (HelloWorld) context.getBean("helloBean");
		obj.printHello();
	}
}

Linux:~/spring-project:~ $ gradle jar
Linux:~/spring-project:~ $ gradle -PmainClass=com.mycls.App run
```

## via Eclipse

## via IntelliJ


----