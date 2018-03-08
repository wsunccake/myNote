
```
linux:~ $ mkdir mvc1
linux:~ $ cd mvc1/
linux:~/mvc1 $ gradle init
linux:~/mvc1 $ mkdir -p src/main/{java,webapp,resources}
linux:~/mvc1 $ mkdir -p src/main/webapp/WEB-INF

linux:~/mvc1 $ vi build.gradle 
apply plugin: 'java'
apply plugin: 'war'
apply plugin: 'jetty'

// JDK 8
sourceCompatibility = 1.8
targetCompatibility = 1.8

repositories {
    mavenLocal()
    mavenCentral()
}

dependencies {
	compile 'org.springframework:spring-webmvc:4.1.6.RELEASE'
	compile group: 'org.springframework', name: 'spring-test', version: '4.1.6.RELEASE'

	testCompile group: 'junit', name: 'junit', version: '4.4'
	testCompile "javax.servlet:javax.servlet-api:3.1.0"
}


// Embeded Jetty for testing
jettyRun{
	contextPath = "mvc1"
	httpPort = 8080
}

jettyRunWar{
	contextPath = "mvc1"
	httpPort = 8080
}

linux:~/mvc1 $ mkdir src/main/java/mypkg
linux:~/mvc1 $ vi src/main/java/mypkg/WelcomeController.java
package mypkg;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;

@Controller
public class WelcomeController {

	@RequestMapping(value = "/", method = RequestMethod.GET)
	public String home() {
		return "home";
	}

}

linux:~/mvc1 $ mkdir src/main/webapp/WEB-INF/views/jsp
linux:~/mvc1 $ vi src/main/webapp/WEB-INF/views/jsp/home.jsp 
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags"%>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core"%>
<!DOCTYPE html>
<html lang="en">
<head>
<title>Gradle + Spring MVC</title>
</head>

<body>
<p>Hello Spring MVC</p>

</body>
</html>

linux:~/mvc1 $ vi src/main/webapp/WEB-INF/web.xml 
<web-app xmlns="http://java.sun.com/xml/ns/javaee"
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xsi:schemaLocation="http://java.sun.com/xml/ns/javaee
	http://java.sun.com/xml/ns/javaee/web-app_2_5.xsd"
	version="2.5">

	<display-name>Gradle + Spring MVC Hello World + XML</display-name>
	<description>Spring MVC web application</description>

	<!-- For web context -->
	<servlet>
		<servlet-name>hello-dispatcher</servlet-name>
		<servlet-class>
                        org.springframework.web.servlet.DispatcherServlet
                </servlet-class>
		<init-param>
			<param-name>contextConfigLocation</param-name>
			<param-value>/WEB-INF/spring-mvc-config.xml</param-value>
		</init-param>
		<load-on-startup>1</load-on-startup>
	</servlet>

	<servlet-mapping>
		<servlet-name>hello-dispatcher</servlet-name>
		<url-pattern>/</url-pattern>
	</servlet-mapping>

	<!-- For root context -->
	<listener>
		<listener-class>
                  org.springframework.web.context.ContextLoaderListener
                </listener-class>
	</listener>

        <context-param>
                <param-name>contextConfigLocation</param-name>
                <param-value>/WEB-INF/spring-core-config.xml</param-value>
        </context-param>
</web-app>

linux:~/mvc1 $ vi src/main/webapp/WEB-INF/spring-mvc-config.xml 
<beans xmlns="http://www.springframework.org/schema/beans"
	xmlns:context="http://www.springframework.org/schema/context"
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xmlns:mvc="http://www.springframework.org/schema/mvc"
	xsi:schemaLocation="
        http://www.springframework.org/schema/beans
        http://www.springframework.org/schema/beans/spring-beans.xsd
        http://www.springframework.org/schema/mvc
        http://www.springframework.org/schema/mvc/spring-mvc.xsd
        http://www.springframework.org/schema/context
        http://www.springframework.org/schema/context/spring-context.xsd ">

	<context:component-scan base-package="mypkg" />

	<bean class="org.springframework.web.servlet.view.InternalResourceViewResolver">
		<property name="viewClass" value="org.springframework.web.servlet.view.JstlView"/>
		<property name="prefix" value="/WEB-INF/views/jsp/" />
		<property name="suffix" value=".jsp" />
	</bean>
</beans>

linux:~/mvc1 $ vi src/main/webapp/WEB-INF/spring-core-config.xml 
<beans xmlns="http://www.springframework.org/schema/beans"
	xmlns:context="http://www.springframework.org/schema/context"
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xmlns:mvc="http://www.springframework.org/schema/mvc"
	xsi:schemaLocation="
        http://www.springframework.org/schema/beans
        http://www.springframework.org/schema/beans/spring-beans.xsd
        http://www.springframework.org/schema/context
        http://www.springframework.org/schema/context/spring-context.xsd ">

</beans>

# run
linux:~/mvc1 $ gradle jettyRun

# http://localhost:8080/mvc1


linux:~/mvc1 $ mkdir -p src/test/java
linux:~/mvc1 $ cat src/test/java/WelcomeControllerTest.java 
package mypkg;

import static org.junit.Assert.assertEquals;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.view;
import static org.springframework.test.web.servlet.setup.MockMvcBuilders.standaloneSetup;

import org.junit.Test;
import org.springframework.test.web.servlet.MockMvc;

public class WelcomeControllerTest {
	@Test
	public void testHomePage() throws Exception {
		WelcomeController controller = new WelcomeController();
		assertEquals("home", controller.home());

		MockMvc mockMvc = standaloneSetup(controller).build();
		mockMvc.perform(get("/")).andExpect(view().name("home"));
	}
}


# run
linux:~/mvc1$ gradle test
```

