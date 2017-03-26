# JSP

```
linux:~/ex_jsp $ gradle init
linux:~/ex_jsp $ mkdir -p src/main/{java,webapp,resources}
linux:~/ex_jsp $ mkdir -p src/main/webapp/WEB-INF
linux:~/ex_jsp $ mkdir -p src/main/java/mypkg

# build.gradle
linux:~/ex_jsp $ vi build.gradle
apply plugin: 'war'

repositories {
    mavenCentral()
}

dependencies {
   providedCompile   'org.apache.tomcat:tomcat-servlet-api:7.0.37'
   compile 'com.sun.jersey:jersey-bundle:1.17.1'
   compile 'com.sun.faces:jsf-api:2.1.19'
   compile 'com.sun.faces:jsf-impl:2.1.19'
   compile 'org.eclipse.persistence:javax.persistence:2.0.0'
}

# jsp
linux:~/ex_jsp $ vi src/main/webapp/index.jsp 
<%@ page language="java"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
    <title>JSP Demo</title>
</head>
<body>
    <%-- comment --%>
    <% for (int i = 1; i <= 3; i++) { %>
            <%= "Hello, JSP<br/>" %>
    <% } %>
</body>
</html>

# web.xml
linux:~/ex_jsp $ vi src/main/webapp/WEB-INF/web.xml 
<?xml version="1.0" encoding="UTF-8"?>
<web-app xmlns="http://xmlns.jcp.org/xml/ns/javaee"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://xmlns.jcp.org/xml/ns/javaee http://xmlns.jcp.org/xml/ns/javaee/web-app_3_1.xsd"
         version="3.1">
    <welcome-file-list>
        <welcome-file>index.jsp</welcome-file>
    </welcome-file-list>
    <servlet>
        <!-- class name -->
        <servlet-name>HelloServlet</servlet-name>
        <!-- module -->
        <servlet-class>mypkg.HelloServlet</servlet-class>
    </servlet>
    <servlet-mapping>
        <!--  class name -->
        <servlet-name>HelloServlet</servlet-name>
        <!-- url -->
        <url-pattern>/hello</url-pattern>
    </servlet-mapping>
</web-app>

# create war
linux:~/ex_jsp $ gradle war
```


# Servlet

```
linux:~/ex_servlet $ gradle init
linux:~/ex_servlet $ mkdir -p src/main/{java,webapp,resources}
linux:~/ex_servlet $ mkdir -p src/main/webapp/WEB-INF
linux:~/ex_servlet $ mkdir -p src/main/java/mypkg

# build.gradle
linux:~/ex_servlet $ vi build.gradle
apply plugin: 'war'
apply plugin: 'com.bmuschko.tomcat'

repositories {
    mavenCentral()
}

dependencies {
   def tomcatVersion = '7.0.37'
   tomcat "org.apache.tomcat.embed:tomcat-embed-core:${tomcatVersion}",
          "org.apache.tomcat.embed:tomcat-embed-logging-juli:${tomcatVersion}",
          "org.apache.tomcat.embed:tomcat-embed-jasper:${tomcatVersion}"

   providedCompile   "org.apache.tomcat:tomcat-servlet-api:${tomcatVersion}"
   compile 'com.sun.jersey:jersey-bundle:1.17.1'
   compile 'com.sun.faces:jsf-api:2.1.19'
   compile 'com.sun.faces:jsf-impl:2.1.19'
   compile 'org.eclipse.persistence:javax.persistence:2.0.0'
} 

buildscript {
   repositories {
       jcenter()
   }

   dependencies {
       classpath 'com.bmuschko:gradle-tomcat-plugin:2.2.5'
   }
}


# servlet
linux:~/ex_servlet $ vi src/main/java/mypkg/HelloServlet.java 
package mypkg;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.io.PrintWriter;

public class HelloServlet extends HttpServlet {
    String name;
    String content = "<html>" +
            "<head>" +
            "<body>" +
            "<p>Hello," +
            "%s" +
            "</p>" +
            "</body>" +
            "</html>";

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        name = req.getParameter("name");
        resp.setContentType("text/html;charset=UTF=8");
        PrintWriter out = resp.getWriter();
        out.print(String.format(content, name));
        out.close();
    }
}

# web.xml
linux:~/ex_servlet $ vi src/main/webapp/WEB-INF/web.xml 
<?xml version="1.0" encoding="UTF-8"?>
<web-app xmlns="http://xmlns.jcp.org/xml/ns/javaee"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://xmlns.jcp.org/xml/ns/javaee http://xmlns.jcp.org/xml/ns/javaee/web-app_3_1.xsd"
         version="3.1">
    <servlet>
        <!-- class name -->
        <servlet-name>HelloServlet</servlet-name>
        <!-- module -->
        <servlet-class>mypkg.HelloServlet</servlet-class>
    </servlet>
    <servlet-mapping>
        <!--  class name -->
        <servlet-name>HelloServlet</servlet-name>
        <!-- url -->
        <url-pattern>/hello</url-pattern>
    </servlet-mapping>
</web-app>

# create war
linux:~/ex_servlet $ gradle war

# run tomcat
linux:~/ex_servlet $ gradle tomcatRun
```