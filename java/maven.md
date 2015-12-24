# maven


## Install

	rhel:~ # wget http://ftp.tc.edu.tw/pub/Apache/maven/maven-3/3.3.9/binaries/apache-maven-3.3.9-bin.tar.gz
	rhel:~ # tar zxf apache-maven-3.3.9-bin.tar.gz -C /opt
	rhel:~ # ln -s /opt/apache-maven-3.3.9 /opt/apache-maven

	rhel:~ # export M2_HOME=/opt/apache-maven
	rhel:~ # export PATH=$PATH:$M2_HOME/bin

	rhel:~ # echo $JAVA_HOME
	rhel:~ # mvn -v

	rhel:~ # export MAVEN_OPTS="-Xms512m"

maven 會將需要的 jar 下載在 $basedir/.m2/repository/org/apache/maven (預設 $basedir 為使用者家目錄下)


## Quick Start


### Create Project

	rhel:~ # mvn archetype:generate \
	> -DgroupId=com.mycompany.app \
	> -DartifactId=my-app \
	> -DarchetypeArtifactId=maven-archetype-quickstart \
	> -DinteractiveMode=false

groupId 和 artifactId 套件資訊 
archetypeArtifactId 套件使用模版 (專案種類) 

	rhel:~ # tree my-app/
	my-app/
	|-- pom.xml
	`-- src
	    |-- main
	    |   `-- java
	    |       `-- com
	    |           `-- mycompany
	    |               `-- app
	    |                   `-- App.java
	    `-- test
	        `-- java
	            `-- com
	                `-- mycompany
	                    `-- app
	                        `-- AppTest.java
	rhel:~ # cat my-app/src/main/java/com/mycompany/app/App.java

src/main/java        放置專案原始碼
src/test/java        放置單元測試用原始碼
src/main/resources   放置設定檔, 例如 log4j.properties
src/test/resources   放置測試用設定檔, 如同測試程式本身不會被打包進 jar
target               distributable JAR
target/classes       complied byte code


### Build Project

	rhel:~/my-app $ mvn compile    # compile 就會產生對應的 class file
	rhel:~/my-app $ mvn package    # package 就是 build 
	rhel:~/my-app $ java -cp target/my-app-1.0-SNAPSHOT.jar com.mycompany.app.App

	rhel:~/my-app $ tree
	.
	|-- pom.xml
	|-- src
	|   |-- main
	|   |   `-- java
	|   |       `-- com
	|   |           `-- mycompany
	|   |               `-- app
	|   |                   `-- App.java
	|   `-- test
	|       `-- java
	|           `-- com
	|               `-- mycompany
	|                   `-- app
	|                       `-- AppTest.java
	`-- target
	    |-- classes
	    |   `-- com
	    |       `-- mycompany
	    |           `-- app
	    |               `-- App.class
	    |-- maven-archiver
	    |   `-- pom.properties
	    |-- maven-status
	    |   `-- maven-compiler-plugin
	    |       |-- compile
	    |       |   `-- default-compile
	    |       |       |-- createdFiles.lst
	    |       |       `-- inputFiles.lst
	    |       `-- testCompile
	    |           `-- default-testCompile
	    |               |-- createdFiles.lst
	    |               `-- inputFiles.lst
	    |-- my-app-1.0-SNAPSHOT.jar
	    |-- surefire-reports
	    |   |-- com.mycompany.app.AppTest.txt
	    |   `-- TEST-com.mycompany.app.AppTest.xml
	    `-- test-classes
	        `-- com
	            `-- mycompany
	                `-- app
	                    `-- AppTest.class


### Project Object Model / POM

	rhel:~/my-app # cat pom.xml 
	<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	  xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/maven-v4_0_0.xsd">
	  <modelVersion>4.0.0</modelVersion>
	  <groupId>com.mycompany.app</groupId>
	  <artifactId>my-app</artifactId>
	  <packaging>jar</packaging>
	  <version>1.0-SNAPSHOT</version>
	  <name>my-app</name>
	  <url>http://maven.apache.org</url>
	  <dependencies>
	    <dependency>
	      <groupId>junit</groupId>
	      <artifactId>junit</artifactId>
	      <version>3.8.1</version>
	      <scope>test</scope>
	    </dependency>
	  </dependencies>
	</project>

這樣是一組 dependency

	    <dependency>
	      <groupId>junit</groupId>
	      <artifactId>junit</artifactId>
	      <version>3.8.1</version>
	    </dependency>

## Command

	rhel:~ # mvn -h
	rhel:~ # mvn help system
	rhel:~ # mvn complie
	rhel:~ # mvn package
	rhel:~ # mvn clean