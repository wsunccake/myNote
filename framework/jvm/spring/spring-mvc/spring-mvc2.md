# Spring MVC

```
linux:~/apache-tomcat $ mkdir webapps/spring-mvc-ex1
linux:~/apache-tomcat $ mkdir -p webapps/spring-mvc-ex1/src/mypkg

# controller
linux:~/apache-tomcat $ vi webapps/spring-mvc-ex1/src/mypkg/HelloWorldController.java 
package mypkg;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.springframework.web.servlet.ModelAndView;
import org.springframework.web.servlet.mvc.AbstractController;

public class HelloWorldController extends AbstractController {

   @Override
   protected ModelAndView handleRequestInternal(HttpServletRequest request,
         HttpServletResponse response) throws Exception {

      ModelAndView model = new ModelAndView("HelloWorldPage");
      model.addObject("msg", "hello world");

      return model;
   }
}

linux:~/apache-tomcat $ mkdir -p webapps/spring-mvc-ex1/WEB-INF

# web.xml
linux:~/apache-tomcat $ vi webapps/spring-mvc-ex1/WEB-INF/web.xml 
<web-app id="WebApp_ID" version="2.4"
   xmlns="http://java.sun.com/xml/ns/j2ee" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
   xsi:schemaLocation="http://java.sun.com/xml/ns/j2ee 
   http://java.sun.com/xml/ns/j2ee/web-app_2_4.xsd">

   <display-name>Spring Web MVC Application</display-name>

   <servlet>
      <servlet-name>mvc-dispatcher</servlet-name>
      <servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
      <load-on-startup>1</load-on-startup>
   </servlet>

   <servlet-mapping>
      <servlet-name>mvc-dispatcher</servlet-name>
      <url-pattern>*.html</url-pattern>
   </servlet-mapping>
</web-app>

# dispatcher config/bean
linux:~/apache-tomcat $ vi webapps/spring-mvc-ex1/WEB-INF/mvc-dispatcher-servlet.xml 
<beans xmlns="http://www.springframework.org/schema/beans"
   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
   xsi:schemaLocation="http://www.springframework.org/schema/beans 
   http://www.springframework.org/schema/beans/spring-beans-2.5.xsd">

   <bean id="viewResolver" class="org.springframework.web.servlet.view.InternalResourceViewResolver">
      <property name="prefix">
         <value>/WEB-INF/pages/</value>
      </property>
      <property name="suffix">
         <value>.jsp</value>
      </property>
   </bean>

   <bean name="/welcome.html" class="mypkg.HelloWorldController" />
</beans>

linux:~/apache-tomcat $ mkdir -p webapps/spring-mvc-ex1/WEB-INF/pages
# viewer/jsp
linux:~/apache-tomcat$ cat webapps/spring-mvc-ex1/WEB-INF/pages/HelloWorldPage.jsp 
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core"%>
<html>
<body>
   <h1>Spring MVC Hello World Example</h1>

   <h2>${msg}</h2>

</body>
</html>

linux:~/apache-tomcat $ mkdir -p webapps/spring-mvc-ex1/WEB-INF/lib
# download jar in lib
aopalliance-1.0.jar
commons-logging-1.1.1.jar
jstl-1.2.jar
spring-beans-2.5.6.jar
spring-context-2.5.6.jar
spring-context-support-2.5.6.jar
spring-core-2.5.6.jar
spring-web-2.5.6.jar
spring-webmvc-2.5.6.jar

linux:~/apache-tomcat $ mkdir -p webapps/spring-mvc-ex1/WEB-INF/classes
# compile
linux:~/apache-tomcat$ javac -cp `find ~/apache-tomcat/lib ~/apache-tomcat/webapps/spring-mvc-ex1/WEB-INF/lib -name \*.jar | tr '\n' :` -d webapps/spring-mvc-ex1/WEB-INF/classes webapps/spring-mvc-ex1/src/mypkg/HelloWorldController.java

# run tomcat
linux:~/apache-tomcat $ ./bin/startup.sh
linux:~/apache-tomcat $ ./bin/stop

# 在啟動 tomcat 時, 可以使用瀏覽器看
# http://localhost:8080/spring-mvc-ex1/welcome.html
```


# Spring MVC via maven


# Spring MVC via gradle

```
linux:~ $ mkdir spring-mvc-ex3
linux:~ $ cd spring-mvc-ex3/
linux:~/spring-mvc-ex3 $ gradle init

linux:~/spring-mvc-ex3 $ mkdir -p src/main/{java,webapp,resources}
linux:~/spring-mvc-ex3 $ mkdir -p src/main/webapp/WEB-INF
linux:~/spring-mvc-ex3 $ mkdir -p src/main/java/mypkg

# build.gradle
linux:~/spring-mvc-ex3 $ vi build.gradle 
apply plugin: 'war'

repositories {
    mavenCentral()
}

dependencies {
   compile group: 'org.springframework', name: 'spring-webmvc', version: '2.5.6'
   compile group: 'javax.servlet', name: 'jstl', version: '1.2'
   compile group: 'javax.servlet', name: 'servlet-api', version: '2.5'

}

# controller
linux:~/spring-mvc-ex3 $ vi src/main/java/mypkg/HelloWorldController.java 
package mypkg;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.springframework.web.servlet.ModelAndView;
import org.springframework.web.servlet.mvc.AbstractController;

public class HelloWorldController extends AbstractController {

   @Override
   protected ModelAndView handleRequestInternal(HttpServletRequest request,
         HttpServletResponse response) throws Exception {

      ModelAndView model = new ModelAndView("HelloWorldPage");
      model.addObject("msg", "hello world");

      return model;
   }
}

# web.xml
linux:~/spring-mvc-ex3 $ cat src/main/webapp/WEB-INF/web.xml 
<web-app id="WebApp_ID" version="2.4"
   xmlns="http://java.sun.com/xml/ns/j2ee" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
   xsi:schemaLocation="http://java.sun.com/xml/ns/j2ee 
   http://java.sun.com/xml/ns/j2ee/web-app_2_4.xsd">

   <display-name>Spring Web MVC Application</display-name>

   <servlet>
      <servlet-name>mvc-dispatcher</servlet-name>
      <servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
      <load-on-startup>1</load-on-startup>
   </servlet>

   <servlet-mapping>
      <servlet-name>mvc-dispatcher</servlet-name>
      <url-pattern>*.html</url-pattern>
   </servlet-mapping>

</web-app>

# dispatcher config/bean
linux:~/spring-mvc-ex3 $ cat src/main/webapp/WEB-INF/mvc-dispatcher-servlet.xml 
<beans xmlns="http://www.springframework.org/schema/beans"
   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
   xsi:schemaLocation="http://www.springframework.org/schema/beans 
   http://www.springframework.org/schema/beans/spring-beans-2.5.xsd">

   <bean id="viewResolver" class="org.springframework.web.servlet.view.InternalResourceViewResolver">
      <property name="prefix">
         <value>/WEB-INF/pages/</value>
      </property>
      <property name="suffix">
         <value>.jsp</value>
      </property>
   </bean>

   <bean name="/welcome.html" class="mypkg.HelloWorldController" />
</beans>

# viewer/jsp
linux:~/spring-mvc-ex3$ cat src/main/webapp/WEB-INF/pages/HelloWorldPage.jsp 
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core"%>
<html>
<body>
   <h1>Spring MVC Hello World Example</h1>

   <h2>${msg}</h2>

</body>
</html>

# create war
linux:~/spring-mvc-ex3 $ gradle war
```