# Java #


## Install ##

先到 [Oracle](http://www.oracle.com/technetwork/java/javase/downloads/index.html) 下載 JDK (Java Development Kit) 不是 JRE (Java Runtime Environment). 有 ME (Micro Edition), SE (Standard Edition) 和 EE (Enterprise Edition) 版本, 選擇 SE 就
可以


### Environmnet ###

`Unix`

	# for sh/bash
	Linux:~ $ export JAVA_HOME=/usr/lib/java
	Linux:~ $ export CLASSPATH=$JAVA_HOME/lib
	Linux:~ $ PATH=$PATH:$JAVA_HOME/bin

	# for csh/tcsh
	Linux:~ $ setenv JAVA_HOME /usr/lib/java
	Linux:~ $ setenv CLASSPATH ${JAVA_HOME}/lib
	Linux:~ $ set path = ( $path ${JAVA_HOME}/bin )


`Windows`

	JAVA_HOME="C:\Program File\Java\jdk"
	CLASSPATH=%JAVA_HOME%\lib
	path=%path;%JAVA_HOME%\bin


### Test ###

安裝完之後, 可寫個 HelloWorld.java 來測試.

	Linux:~ $ cat HelloWorld.java
	public class HelloWorld {
	    public static void main(String[] args) {
	        System.out.println("Hello World!");
	    }
	}

注意, HelloWorld.java 檔名有分大小寫, 且 HelloWorld 除了是檔案名稱 (file name) 之外還是類別名稱 (class name).

	Linux:~ $ javac HelloWorld.java # java 編譯成 class
	Linux:~ $ java HelloWorld # 執行 class

使用 javac, 將 HelloWorld.javac 編譯成 HelloWorld.class, 使用 java 執行 HelloWorld.class


### Compile ###

source         vm             run
      javac            java
.java  --->   .class   --->


`compile java`

	Linux:~ $ javac [-cp classpath] -d [output_dir] src.java # compile, 將 .java 編譯成 .class
	Linux:~ $ java  [-cp classpath] src # run, 執行.class


`generate jar`

	Linux:~ $ jar cf src.jar -C out_dir
	Linux:~ $ jar tf src.jar
	Linux:~ $ jar xf src.jar


### jar ###

除了 source code 之外, 還可以將 class 打包成 jar, 給其他人使用

`Hi.class`

```java
public class Hi {
    String name;

    public Hi(String name) {
        this.name = name;
    }

    public Hi() {
        this("guy");
    }

    @Override
    public String toString() {
        return "Hi, " + name ;
    }
}
```


`Main.class`

```java
public class Main {
    public static void main(String[] args){
      Hi h = new Hi();
      System.out.println(h);
    }
}
```

`compile & run`

	Linux:~ $ jar cf Hi.jar Hi.java
	Linux:~ $ javac -cp ./Hi.jar Main.java
	Linux:~ $ java Main


--------


## Data Type ##


### premitive type ###

| type 		 | default 	 | range 						 |
| ---------- | --------- | ----------------------------- |
| boolean 	 | false 	 | 								 |
| byte    	 | 0		 | 1 byte  / -2^7 ~ 2^7 - 1 	 |
| char    	 | \u0000 	 | 2 bytes 						 |
| short   	 | 0 		 | 2 bytes / -2^15 ~ 2^15 - 1 	 |
| int     	 | 0 		 | 4 bytes / -2^31 ~ 2^31 - 1 	 |
| long    	 | 0L 		 | 8 bytes / -2^63 ~ 2^63 - 1 	 |
| float   	 | 0.0f 	 | 4 bytes / 32 bits 			 |
| double  	 | 0.0.d 	 | 8 bytes / 64 bits 			 |


### autobox ###

`Test.java`

```Java
public class Test {
    public static void main(String[] args) {
        int i = 1;
        int j = 2;
        System.out.println("i = " + i);
        System.out.println("i + j = " + i + j); # 出現結果非 i + j = 3, 而是 i + j = 12
        System.out.println("i + j = " + (i + j)); # 出現結果非 i + j = 3
    }
}
```

## Operator ##


### assignment ###

=

### mathematical operator ###

+, -. *, /, %,
+=, -=. *=, /=, %=,

### increment and decrement ###

++, --


### relational operator ###

<, >, <=. >=, ==, !=


### logical operator ###

&&, ||, !
short-circuiting

### bitwise operator ###

&, |, ^

### shift operator ###

<<, >>, >>>, <<=, >>=, >>>=

### literal ###

### exponential notation ###

e

### ternary operator ###

?:

```
i < 10 ? 10 * i : 0.1 * i
```

### casting operator ###

()

```
4 / 5
(float) 4 / 5
```

## Condition ##

### if else ###

### switch case ###


`SwitchDemo.java`

```Java
public class SwitchDemo {
    public enum PowerStatus {
        POWER_ON, POWER_OFF;

        private int flag;

        PowerStatus(int flag) {
            this.flag = flag;
        }

        public int getFlag() {
            return flag;
        }
    }

    public static void main(String[] args) {
        int value = 1;
        switch (value) {
            case 1:
                System.out.println("Power on");
                break;
            case 0:
                System.out.println("Power off");
                break;
            default:
                System.out.println("Unknown action");
        }

        PowerStatus status = PowerStatus.POWER_OFF;
        switch (status) {
            case POWER_ON:
                System.out.println("Power on");
                break;
            case POWER_OFF:
                System.out.println("Power off");
                break;
            default:
                System.out.println("Unknown action");
        }
        System.out.println("The flag: " + status.getFlag());
    }
}
```

## Loop ##

### for ###

### foreach ###

### while ###

## Method ##

## Class ##

## Inheritance ##

## Generics ##

## Interface ##

## Container ##


--------


## String ##

## File I/O ##

## Command ##

## thread / process ##

## reflection ##

## anatation ##


--------


## JavaFX / Swing ##

## Serverlet ##