# Annotation Config

## @Required

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
linux:~/project # vi src/main/java/com/mycls/Student.java 
package com.mycls;

import org.springframework.beans.factory.annotation.Required;

public class Student {
   private Integer age;
   private String name;

   @Required
   public void setAge(Integer age) {
      this.age = age;
   }
   public Integer getAge() {
      return age;
   }
   
   @Required
   public void setName(String name) {
      this.name = name;
   }
   public String getName() {
      return name;
   }
}
```

`config`

```bash
linux:~/project # vi src/main/resources/Beans.xml 
<?xml version = "1.0" encoding = "UTF-8"?>

<beans xmlns = "http://www.springframework.org/schema/beans"
   xmlns:xsi = "http://www.w3.org/2001/XMLSchema-instance"
   xmlns:context = "http://www.springframework.org/schema/context"
   xsi:schemaLocation = "http://www.springframework.org/schema/beans
   http://www.springframework.org/schema/beans/spring-beans-3.0.xsd
   http://www.springframework.org/schema/context
   http://www.springframework.org/schema/context/spring-context-3.0.xsd">
   <context:annotation-config/>
   <bean id = "student" class = "com.mycls.Student">
      <property name = "name" value = "Zara"/>
      <property name = "age"  value = "11"/>
   </bean>
</beans>
```

`main class`

```bash
linux:~/project # vi src/main/java/com/mycls/MainApp.java 
package com.mycls;

import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

public class MainApp {
   public static void main(String[] args) {
      ApplicationContext context = new ClassPathXmlApplicationContext("Beans.xml");     
      Student student = (Student) context.getBean("student");
      System.out.println("Name : " + student.getName() );
      System.out.println("Age : " + student.getAge() );
   }
}
```


---

## @Autowired


### on Constructor

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
linux:~/project # vi src/main/java/com/mycls/SpellChecker.java 
package com.mycls;

public class SpellChecker {
   public SpellChecker(){
      System.out.println("Inside SpellChecker constructor.");
   }
   public void checkSpelling() {
      System.out.println("Inside checkSpelling.");
   }
}
```

```bash
linux:~/project # vi src/main/java/com/mycls/TextEditor.java 
package com.mycls;

import org.springframework.beans.factory.annotation.Autowired;

public class TextEditor {
  private SpellChecker spellChecker;

  @Autowired
  public TextEditor(SpellChecker spellChecker) {
    System.out.println("Inside TextEditor constructor.");
    this.spellChecker = spellChecker;
  }
  public void spellCheck() {
    spellChecker.checkSpelling();
  }
}
```

`config`

```bash
linux:~/project # vi src/main/resources/Beans.xml 
<?xml version="1.0" encoding="UTF-8"?>

<beans xmlns="http://www.springframework.org/schema/beans"
   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
   xmlns:context="http://www.springframework.org/schema/context"
   xsi:schemaLocation="http://www.springframework.org/schema/beans
   http://www.springframework.org/schema/beans/spring-beans.xsd
   http://www.springframework.org/schema/context
   http://www.springframework.org/schema/context/spring-context.xsd">
   <context:annotation-config/>
   <bean id="textEditor" class="com.mycls.TextEditor"></bean>
   <bean id="spellChecker" class="com.mycls.SpellChecker"></bean>
</beans>
```

`main class`

```bash
linux:~/project # vi src/main/java/com/mycls/MainApp.java 
package com.mycls;

import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

public class MainApp {
   public static void main(String[] args) {
      ApplicationContext context = new ClassPathXmlApplicationContext("Beans.xml");
      TextEditor te = (TextEditor) context.getBean("textEditor");
      te.spellCheck();
   }
}
```

### on Setter

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
linux:~/project # vi src/main/java/com/mycls/SpellChecker.java 
package com.mycls;

public class SpellChecker {
   public SpellChecker(){
      System.out.println("Inside SpellChecker constructor.");
   }
   public void checkSpelling() {
      System.out.println("Inside checkSpelling.");
   }
}
```

```bash
linux:~/project # vi src/main/java/com/mycls/TextEditor.java 
package com.mycls;

import org.springframework.beans.factory.annotation.Autowired;

public class TextEditor {
  private SpellChecker spellChecker;

  @Autowired
  public void setSpellChecker( SpellChecker spellChecker ){
    this.spellChecker = spellChecker;
  }
  public SpellChecker getSpellChecker( ) {
    return spellChecker;
  }
  public void spellCheck() {
    spellChecker.checkSpelling();
  }
}
```

`config`

```bash
linux:~/project # vi src/main/resources/Beans.xml 
<?xml version="1.0" encoding="UTF-8"?>

<beans xmlns="http://www.springframework.org/schema/beans"
   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
   xmlns:context="http://www.springframework.org/schema/context"
   xsi:schemaLocation="http://www.springframework.org/schema/beans
   http://www.springframework.org/schema/beans/spring-beans.xsd
   http://www.springframework.org/schema/context
   http://www.springframework.org/schema/context/spring-context.xsd">
   <context:annotation-config/>
   <bean id="textEditor" class="com.mycls.TextEditor"></bean>
   <bean id="spellChecker" class="com.mycls.SpellChecker"></bean>
</beans>
```

`main class`

```bash
linux:~/project # vi src/main/java/com/mycls/MainApp.java 
package com.mycls;

import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

public class MainApp {
   public static void main(String[] args) {
      ApplicationContext context = new ClassPathXmlApplicationContext("Beans.xml");
      TextEditor te = (TextEditor) context.getBean("textEditor");
      te.spellCheck();
   }
}
```

### on Property

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
linux:~/project # vi src/main/java/com/mycls/SpellChecker.java 
package com.mycls;

public class SpellChecker {
   public SpellChecker(){
      System.out.println("Inside SpellChecker constructor.");
   }
   public void checkSpelling() {
      System.out.println("Inside checkSpelling.");
   }
}
```

```bash
linux:~/project # vi src/main/java/com/mycls/TextEditor.java 
package com.mycls;

import org.springframework.beans.factory.annotation.Autowired;

public class TextEditor {
  @Autowired
  private SpellChecker spellChecker;

  public TextEditor() {
    System.out.println("Inside TextEditor constructor." );
  }
   
  public SpellChecker getSpellChecker( ){
    return spellChecker;
  }
   
  public void spellCheck(){
    spellChecker.checkSpelling();
  }
}
```

`config`

```bash
linux:~/project # vi src/main/resources/Beans.xml 
<?xml version="1.0" encoding="UTF-8"?>

<beans xmlns="http://www.springframework.org/schema/beans"
   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
   xmlns:context="http://www.springframework.org/schema/context"
   xsi:schemaLocation="http://www.springframework.org/schema/beans
   http://www.springframework.org/schema/beans/spring-beans.xsd
   http://www.springframework.org/schema/context
   http://www.springframework.org/schema/context/spring-context.xsd">
   <context:annotation-config/>
   <bean id="textEditor" class="com.mycls.TextEditor"></bean>
   <bean id="spellChecker" class="com.mycls.SpellChecker"></bean>
</beans>
```

`main class`

```bash
linux:~/project # vi src/main/java/com/mycls/MainApp.java 
package com.mycls;

import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

public class MainApp {
   public static void main(String[] args) {
      ApplicationContext context = new ClassPathXmlApplicationContext("Beans.xml");
      TextEditor te = (TextEditor) context.getBean("textEditor");
      te.spellCheck();
   }
}
```


---

## @Qualifier

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
linux:~/project # vi src/main/java/com/mycls/Student.java
package com.mycls;

import org.springframework.beans.factory.annotation.Required;

public class Student {
  private Integer age;
  private String name;

  public void setAge(Integer age) {
    this.age = age;
  }
  public Integer getAge() {
    return age;
  }
   
  public void setName(String name) {
    this.name = name;
  }
  public String getName() {
    return name;
  }
}
```

```bash
linux:~/project # vi src/main/java/com/mycls/Profile.java
package com.mycls;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;

public class Profile {
  @Autowired
  @Qualifier("student1")
  private Student student;

  public Profile(){
    System.out.println("Inside Profile constructor." );
  }
  public void printAge() {
    System.out.println("Age : " + student.getAge() );
  }
  public void printName() {
    System.out.println("Name : " + student.getName() );
  }
}
```

`config`

```bash
linux:~/project # vi src/main/resources/Beans.xml 
<?xml version = "1.0" encoding = "UTF-8"?>

<beans xmlns = "http://www.springframework.org/schema/beans"
   xmlns:xsi = "http://www.w3.org/2001/XMLSchema-instance"
   xmlns:context = "http://www.springframework.org/schema/context"
   xsi:schemaLocation = "http://www.springframework.org/schema/beans
   http://www.springframework.org/schema/beans/spring-beans-3.0.xsd
   http://www.springframework.org/schema/context
   http://www.springframework.org/schema/context/spring-context-3.0.xsd">
   <context:annotation-config/>
   <bean id = "profile" class = "com.mycls.Profile"></bean>
   <bean id = "student1" class = "com.mycls.Student">
      <property name = "name" value = "Zara" />
      <property name = "age" value = "11"/>
   </bean>
   <bean id = "student2" class = "com.mycls.Student">
      <property name = "name" value = "Nuha" />
      <property name = "age" value = "2"/>
   </bean>
</beans>
```

`main class`

```bash
linux:~/project # vi src/main/java/com/mycls/MainApp.java 
package com.mycls;

import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

public class MainApp {
   public static void main(String[] args) {
      ApplicationContext context = new ClassPathXmlApplicationContext("Beans.xml");
      Profile profile = (Profile) context.getBean("profile");
      profile.printAge();
      profile.printName();
   }
}
```


---

## JSR-250

### @PostConstruct & @PreDestroy

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

import javax.annotation.*;

public class HelloWorld {
  private String message;

  public void setMessage(String message){
    this.message  = message;
  }
  public String getMessage(){
    System.out.println("Your Message : " + message);
    return message;
  }
   
  @PostConstruct
  public void init(){
    System.out.println("Bean is going through init.");
  }
   
  @PreDestroy
  public void destroy(){
    System.out.println("Bean will destroy now.");
  }
}
```

`config`

```bash
linux:~/project # vi src/main/resources/Beans.xml 
<?xml version = "1.0" encoding = "UTF-8"?>

<beans xmlns = "http://www.springframework.org/schema/beans"
   xmlns:xsi = "http://www.w3.org/2001/XMLSchema-instance"
   xmlns:context = "http://www.springframework.org/schema/context"
   xsi:schemaLocation = "http://www.springframework.org/schema/beans
   http://www.springframework.org/schema/beans/spring-beans-3.0.xsd
   http://www.springframework.org/schema/context
   http://www.springframework.org/schema/context/spring-context-3.0.xsd">
   <context:annotation-config/>
   <bean id = "helloWorld" class = "com.mycls.HelloWorld"
      init-method = "init" destroy-method = "destroy">
      <property name = "message" value = "Hello World!"/>
   </bean>   </bean>
</beans>
```

`main class`

```bash
linux:~/project # vi src/main/java/com/mycls/MainApp.java 
package com.mycls;

import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

public class MainApp {
   public static void main(String[] args) {
      AbstractApplicationContext context = new ClassPathXmlApplicationContext("Beans.xml");
      HelloWorld obj = (HelloWorld) context.getBean("helloWorld");
      obj.getMessage();
      context.registerShutdownHook();
   }
}
```

### @Resource
