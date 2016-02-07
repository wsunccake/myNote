# JSP


## Introduction

JSP（全稱JavaServer Pages）是由Sun Microsystems公司倡導和許多公司參與共同建立的一種使軟體開發者可以響應用戶端請求，而動態生成HTML、XML或其他格式文件的Web網頁的技術標準。 JSP技術是以Java語言作為手稿語言的，JSP網頁為整個伺服器端的Java庫單元提供了一個介面來服務於HTTP的應用程式。

JSP使Java代碼和特定的預定義動作可以嵌入到靜態頁面中。 JSP句法增加了被稱為JSP動作的XML標籤，它們用來呼叫內建功能。另外，可以建立JSP標籤庫，然後像使用標準HTML或XML標籤一樣使用它們。標籤庫提供了一種和平台無關的擴充功能伺服器效能的方法。

JSP被JSP編譯器編譯成Java Servlets。一個JSP編譯器可以把JSP編譯成JAVA代碼寫的servlet然後再由JAVA編譯器來編譯成機器碼，也可以直接編譯成二進位碼。

## Basic


### Syntax

| synatx 		 | example 						 |
| -------------- | ----------------------------- |
| Comment 		 | <%-- comments --> 			 |
| Declaration 	 | <%! Java Declaration %> 		 |
| Directive 	 | <%@ page, include ... %> 	 |
| Expression 	 | <%= Java Expression %> 		 |
| Scriptlet 	 | <% Java Statement(s) %> 		 |

[Java Server-side Programming
Getting started with JSP by Examples](https://www3.ntu.edu.sg/home/ehchua/programming/java/JSPByExample.html)

```
Linux:~ # tree -L 1 -d ~/apache-tomcat
~/apache-tomcat
├── bin
├── conf
├── lib
├── logs
├── temp
├── webapps
└── work

Linux:~ # tree -L 1 -d ~/apache-tomcat/webapps
~/apache-tomcat/webapps
├── docs
├── examples
├── host-manager
├── manager
└── ROOT

Linux:~ # mkdir -p ~/apache-tomcat/webapps/demo/WEB-INF

Linux:~ # mkdir -p ~/apache-tomcat/webapps/demo/demo.jsp
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

Linux:~ # cat ~/apache-tomcat/webapps/demo/WEB-INF/web.xml
<?xml version="1.0" encoding="GBK"?>
<web-app xmlns="http://xmlns.jcp.org/xml/ns/javaee"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://xmlns.jcp.org/xml/ns/javaee
    http://xmlns.jcp.org/xml/ns/javaee/web-app_3_1.xsd"
    version="3.1">
    <!-- 設定 index page -->
    <welcome-file-list>
        <welcome-file>demo.jsp</welcome-file>
    </welcome-file-list>
</web-app>

Linux:~ # ls ~/apache-tomcat/work/Catalina/localhost/demo/org/apache/jsp
```

使用 Browser 連 http://localhost:8080/demo 或 http://localhost:8080/demo/demo.jsp


### Action

| action 			 | description 											 |
| ------------------ | ----------------------------------------------------- |
| jsp:include 		 | 處理 JSP 或 Servlet 後, 控制權交還給當前 JSP 				 |
| jsp:param 		 | 在 jsp:include, jsp:forward或jsp:params 間傳遞參數使用 	 |
| jsp:forward 		 | 處理 JSP 或 Servlet 後, 控制權不會交還給當前 JSP 			 |
| jsp:plugin 		 | 針對 Browser 產生 Applet 								 |
| jsp:fallback 		 | 瀏覽器不支援 Applets 會顯示內容 							 |
| jsp:getProperty 	 | 從 JavaBean 取得屬性 									 |
| jsp:setProperty 	 | 設定 JavaBean 屬性 									 |
| jsp:useBean 		 | 建立/複製 JavaBean 到JSP 								 |

jsp:forward 範例

```
Linux:~ # cat ~/apache-tomcat/webapps/demo/demo-form.jsp
<%@ page language="java"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
    <title>form</title>
</head>
<body>
    <form id="login" method="post" action="demo-forward.jsp">
        Username: <input type="text" name="user">
        <input type="submit">
    </form>
</body>
</html>

Linux:~ # cat ~/apache-tomcat/webapps/demo/demo-forward.jsp
<%@ page language="java"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
    <title>forward page</title>
</head>
<body>
    <jsp:forward page="demo-result.jsp">
        <jsp:param name="age" value="10" />
    </jsp:forward>
</body>
</html>

Linux:~ # cat ~/apache-tomcat/webapps/demo/demo-result.jsp
<%@ page language="java"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
    <title>result page</title>
</head>
<body>
    Hello
    <%= request.getParameter("user") %>,
    <%= request.getParameter("age") %>
</body>
</html>
```

使用 Browser 連 http://localhost:8080/demo/demo-form.jsp

jsp:useBean, jsp:getProperty, jsp:setProperty 範例


```
Linux:~ # cat ~/apache-tomcat/webapps/demo/demo-class.jsp
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <title>jsp class</title>
</head>
<body>
    <%@page import="mypackage.*" %>
    <%
        Person p = new Person("Johnnie");
        p.setAge(11);
    %>
    <p>
    Hi: <%= p.getName() %>, Age: <%= p.getAge() %>
    </p>
</body>
</html>

Linux:~ # cat ~/apache-tomcat/webapps/demo/demo-bean.jsp
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <title>jsp bean</title>
</head>
<body>
    <jsp:useBean id="p" class="mypackage.Person" scope="page">
        <jsp:setProperty name="p" property="name" value="Johnnie" />
        <jsp:setProperty name="p" property="age" value="11" />
    </jsp:useBean>
    <p>
        Hi: <jsp:getProperty name="p" property="name" />, Age: <jsp:getProperty name="p" property="age" />
    </p>
</body>
</html>
```

Linux:~ # mkdir -p ~/apache-tomcat/webapps/demo/src/mypacakge/
Linux:~ # cat ~/apache-tomcat/webapps/demo/src/mypacakge/Person.java
package mypackage;
public class Person {
    private String name;
    private int age;
    public Person() {}
    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }
    public void setName(String name) { this.name = name; }
    public String getName() { return this.name; }
    public void setAge(int age) { this.age = age; }
    public int getAge() { return this.age; }
}

Linux:~ # mkdir -p ~/apache-tomcat/webapps/demo/lib
Linux:~ # mkdir -p ~/apache-tomcat/webapps/demo/classes
Linux:~ # mkdir -p ~/apache-tomcat/webapps/demo/classes/mypackage

Linux:~ # cd ~/apache-tomcat/webapps/demo
Linux:~/apache-tomcat/webapps/demo # javac -cp servlet-api.jar -d ./classes src/mypacakge/Person.java
Linux:~/apache-tomcat/webapps/demo # jar cf ../demo.war *

----

# Servlet