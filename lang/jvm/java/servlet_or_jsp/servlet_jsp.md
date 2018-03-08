# Java Servlet and JSP


## Tomcat

```
linux:~ $ wget http://apache.stu.edu.tw/tomcat/tomcat-9/v9.0.0.M18/bin/apache-tomcat-9.0.0.M18.tar.gz
linux:~ $ tar zxf apache-tomcat-9.0.0.M18.tar.gz
linux:~ $ ln -s apache-tomcat-9.0.0.M18 apache-tomcat
linux:~ $ cd apache-tomcat

linux:~/apache-tomcat $ tree -L 1
linux:~/apache-tomcat $ tree -L 1 webapps
```


## JSP

```
linux:~/apache-tomcat $ mkdir webapps/jsp

# 建立 jsp
linux:~/apache-tomcat $ vi webapps/jsp/index.jsp 
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

# 設定 web.xml
linux:~/apache-tomcat $ mkdir -p webapps/jsp/WEB-INF
linux:~/apache-tomcat $ vi webapps/jsp/WEB-INF/web.xml
<?xml version="1.0" encoding="UTF-8"?>
<web-app xmlns="http://xmlns.jcp.org/xml/ns/javaee"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://xmlns.jcp.org/xml/ns/javaee
    http://xmlns.jcp.org/xml/ns/javaee/web-app_3_1.xsd"
    version="3.1">
    <!-- 設定 index page -->
    <welcome-file-list>
        <welcome-file>index.jsp</welcome-file>
    </welcome-file-list>
</web-app>

linux:~/apache-tomcat $ tree webapps/jsp

linux:~/apache-tomcat $ ./bin/startup.sh  # 啟動 tomcat
linux:~/apache-tomcat $ ./bin/stop        # 關閉 tomcat

# 在啟動 tomcat 時, 可以使用瀏覽器看
# http://localhost:8080, http://localhost:8080/jsp
```


## Servlet

```
linux:~/apache-tomcat $ mkdir -p webapps/servlet

# 建立 servlet
linux:~/apache-tomcat $ mkdir -p webapps/servlet/src/mypkg
linux:~/apache-tomcat $ vi webapps/servlet/src/mypkg/HelloServlet.java
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

# 設定 web.xml
linux:~/apache-tomcat $ mkdir -p webapps/servlet/WEB-INF
linux:~/apache-tomcat $ mkdir -p webapps/servlet/WEB-INF/classes
linux:~/apache-tomcat $ vi webapps/servlet/WEB-INF/web.xml
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

# 產生 class
linux:~/apache-tomcat $ javac -cp lib/servlet-api.jar -d webapps/servlet/WEB-INF/classes webapps/servlet/src/mypkg/HelloServlet.java

linux:~/apache-tomcat $ ./bin/catalina.sh start # 啟動 tomcat
linux:~/apache-tomcat $ ./bin/catalina.sh stop  # 關閉 tomcat

# http://localhost:8080/servlet/hello, http://localhost:8080/servlet/hello?name=user
```


# VC (use Servlet & JSP)

```
# create project
linux:~/apache-tomcat $ mkdir -p webapps/vc

# servlet
linux:~/apache-tomcat $ mkdir -p webapps/vc/src/mypkg

# dispatcher /router
linux:~/apache-tomcat $ vi webapps/vc/src/mypkg/HelloServlet.java
package mypkg;

import java.io.IOException;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet(name="Hello", urlPatterns={"/hello.do"})
public class HelloServlet extends HttpServlet {
    private Hello hello = new Hello();

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp)
            throws ServletException, IOException {
        String name = req.getParameter("user");
        String message = hello.doHello(name);

        System.out.println("name:" + name);
        System.out.println("message:" + message);
        req.setAttribute("message", message);
        req.getRequestDispatcher("hello.jsp").forward(req, resp);
    }
}

# business logic
linux:~/apache-tomcat $ vi webapps/vc/src/mypkg/Hello.java 
package mypkg;

import java.util.*;

public class Hello {
    private Map<String, String> messages;
    
    public Hello() {
        messages = new HashMap<String, String>();
        messages.put("caterpillar", "Hello");
        messages.put("Justin", "Welcome");
        messages.put("momor", "Hi");
    }

    public String doHello(String user) {
        String message = messages.get(user);
        return message + ", " + user + "!";
    }
}

# view
linux:~/apache-tomcat$ vi webapps/vc/hello.jsp
<%@page contentType="text/html" pageEncoding="UTF-8"%>
<html>
    <head>
        <meta http-equiv="Content-Type"
              content="text/html; charset=UTF-8">
        <title>${param.user}</title>
    </head>
    <body>
        <h1>${message}</h1>
    </body>
</html>

# generate class
linux:~/apache-tomcat $ mkdir -p webapps/vc/WEB-INF/classes
linux:~/apache-tomcat $ javac -cp lib/servlet-api.jar -d webapps/vc/WEB-INF/classes webapps/vc/src/mypkg/HelloServlet.java

# run tomcat
linux:~/apache-tomcat $ ./bin/startup.sh
linux:~/apache-tomcat $ ./bin/stop

# create war
linux:~/apache-tomcat $ cd webapps/vc/
linux:~/apache-tomcat/webapp/vc $ jar cf vc.war webapps/vc/*

# deploy war
linux:~ $ cp vc.war apache-tomcat/webapp/.
```