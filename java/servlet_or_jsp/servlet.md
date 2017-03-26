# Servlet

## Basic

```
Linux:~ # cat ~/apache-tomcat/webapps/demo/src/mypackage/HelloServlet.java
package mypackage;

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

Linux:~ # javac -cp servlet-api.jar -d ~/apache-tomcat/webapps/demo/WEB-INF/classes  ~/apache-tomcat/webapps/demo/src/mypackage/HelloServlet.java

Linux:~ # cat ~/apache-tomcat/webapps/demo/WEB-INF/web.xml
<?xml version="1.0" encoding="UTF-8"?>
<web-app xmlns="http://xmlns.jcp.org/xml/ns/javaee"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://xmlns.jcp.org/xml/ns/javaee http://xmlns.jcp.org/xml/ns/javaee/web-app_3_1.xsd"
         version="3.1">
    <servlet>
        <!-- class name -->
        <servlet-name>HelloServlet</servlet-name>
        <!-- module -->
        <servlet-class>mypackage.HelloServlet</servlet-class>
    </servlet>
    <servlet-mapping>
        <!--  class name -->
        <servlet-name>HelloServlet</servlet-name>
        <!-- url -->
        <url-pattern>/hello</url-pattern>
    </servlet-mapping>
</web-app>
```

使用 Browser 連 http://localhost:8080/demo 或 http://localhost:8080/demo/hello