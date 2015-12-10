# Groovy #


## Install ##

Groovy 可以使用 RPM, DPKG 等系統內建套件直接安裝, 但建議使用 GVM (Groovy enVironment Manager) 安裝管理. 因為 Groovy 會使用到 Java, 須先安裝 JDK (Java Development Kit)

`GVM`

GVM 是 groovy 環境管理工具, 用來安裝設定 groovy 或其他工具

	# 安裝 gvm
	Linux:~ $ curl -s get.gvmtool.net | bash

	Linux:~ $ gvm help
	Linux:~ $ gvm list groovy # 顯示可安裝 groovy 版本

	Linux:~ $ gvm install groovy # 安裝 groovy
	Linux:~ $ gvm install groovy 2.1.9 # 指定版本

	Linux:~ $ gvm use groovy 2.1.9 # 切換版本
	Linux:~ $ gvm default groovy 2.1.9
	Linux:~ $ gvm current groovy

	Liunx:~ $ gvm groovy # 移除 groovy

在安裝 gvm 之後, 會在寫入 $HOME~/.bashrc 環境設定. 而 gvm 套件安裝在 $HOME/.gvm 底下

	Linux~: $ tail ~/.bashrc
	#THIS MUST BE AT THE END OF THE FILE FOR GVM TO WORK!!!
	[[ -s "/home/user/.gvm/bin/gvm-init.sh" ]] && source "/home/user/.gvm/bin/gvm-init.sh

	# 確認環境變數
	Linux:~ $ echo $JAVA_HOME
	Linux:~ $ echo $GROOVY_HOME

`run`

	Linux:~ $ groovy -version # 顯示 groovy 版本

	# command mode
	Linux:~ $ groovy -e "println('Hell, Groovy')"

	# shell mode
	Linux:~ $groovysh

	Groovy Shell (2.4.4, JVM: 1.8.0_45)
	Type ':help' or ':h' for help.
	-------------------------------------------------------------------------------
	groovy:000> println('Hello, Groovy')
	Hello, Groovy
	===> null
	groovy:000> 

	# script mode
	Linux:~ $ cat hello.groovy
	println('Hello, Groovy')

	Linux:~ $ groovy hello.groovy


## Groovy for Java ##


### print, for, foreach ###

`Hello.java`

	public class Hello {
	    public static void main(String[] args) {
	        for (int i =0; i < 3; i++) {
	            System.out.println("i = " + i);
	        }
	        int[] j = {1, 2, 3}
	        for (int i : j) {
	            System.out.println("i = " + i);
	        }
	    }
	}


`Hello.groovy`

	for (int i = 0; i < 3; i++) {
	    System.out.println("i = " + i);
	}

	int[] j = [1, 2, 3]
	for (int i : j) {
	    println "i: $i"
	}

	for (i in 0..2) {
	    println("i = " + i)
	}

	0.upto(2) { println "i = ${it}" }
	3.times { println "i = $it" }


### execution ###

`RunShell.java`

	import java.io.BufferedReader;
	import java.io.IOException;
	import java.io.InputStreamReader;

	public class RunShell {
	    public static void main(String[] args) {
	        try {
	            Process proc = Runtime.getRuntime().exec("ls");
	            BufferedReader result = new BufferedReader(new InputStreamReader(proc.getInputStream()));
	            String line;
	            while ((line = result.readLine()) != null) {
	            System.out.println(line);
	            }
	        }
	        catch(IOException ex) {
	            ex.printStackTrace();
	        }
	    }
	}


`RunShell.groovy`

	println "ls".execute().text


### self-navigation ###

	def foo1(String str) {
	    if (str != null) { str.reverse() }
	}
	println(foo1("abc"))
	println(foo1())

	def foo2(str) {
	    str?.reverse() # 同上
	}
	println(foo2("abc"))
	println(foo2())


### getter, setter ###

`JavaCar.java`

	public class JavaCar {
	    private int miles = 0;
	    private final int year;

	    public JavaCar(int initYear) { this.year = initYear; }
	    public int getMiles() { return this.miles; }
	    private void setMiles(int miles) { this.miles = miles; }
	    public int getYear() { return this.year; }
	    private void drive(dist) { if (dist > 0) this.miles += dist;}

	    public static void main(String[] args) {
	        JavaCar car = new JavaCar(2000);
	        System.out.println("Year: " + car.getYear());
	        System.out.println("Miles: " + car.getMiles());
	        car.drive(10);
	        System.out.println("Miles: " + car.getMiles());
	    }
	}

`GroovyCar`

	class GroovyCar {
	    final year
	    private miles = 0

	    GroovyCar(initYear) { year = initYear}
	    def getMiles() { return miles}
	    private void setMiles(miles) {
	        throw new IllegalAccessException("you're not allow to be change miles")
	    }
	    def drive(dist) { if (dist > 0) miles += dist }

	    public static void main(String[] args) {
	        def car = new GroovyCar(2000)
	        println "Year: $car.year"
	        println "Miles: $car.miles"
	        car.drive(10)
	        println "Miles: $car.miles"
	    }
	}


| keyword 	 | get 	 | set 	 | 
| ---------- | ----- | ----- |
| final 	 | o 	 | 		 |
| public 	 | o 	 | o 	 |
| private 	 |  	 | 		 |


### named parameter ###

`Robot.groovy`

	class Robot {
	    def type, height, width, price
	    def info() {
	        println "robot type: $type, H: $height, W: $width, P: $price"
	    }

	    def access(location, weight, fragile) {
	        println "fragile: $fragile, weight: $weight, location: $location"
	    }
	    def mAccess(Map location, weight, fragile) {
	        println "fragile: $fragile, weight: $weight, location: $location"
	    }
	    def dAccess(x=1, y=2, z=3) {
	        println "x: $x, y: $y, z: $z"
	    }

	    def task(job, String[] items) {
	        println "$job item(s):"
	        items.each {
	            println "$it"
	        }
	    }

	    public static void main(String[] args) {
	        def robot = new Robot(type: "ms", height: 10, width: 40) # constructor vairable
	        robot.info()

	        robot.access([x: 10, y: 20, z: 30], 50, true) # 為宣告型別的第一個 argument 會自動為 hash/dict/map
	        robot.access(x: 10, y: 20, z: 30, 50, true) # 同上
	        robot.access(50, true, [x: 10, y: 20, z: 30]) # 當 argument 中只有一個 map, 會自動變成第一個 argument
	        robot.access(50, true, x: 10, y: 20, z: 30) 

	        robot.mAccess([x: 10, y: 20, z: 30], 50, true)
	        robot.mAccess(50, true, [x: 10, y: 20, z: 30])

	        robot.dAccess() # default value argument
	        robot.dAccess(3, 2, 1)

	        robot.task("wash", "1: disk", "2: bowl", "3: stick") # 無限定 argument
	    }
	}


### enum ###

### @Singleton ###

`Hi.groovy`

	@Singleton
	class Say {
	    def hi () {println "Hi"}
	}

	Say.instance.hi()
	Say.instance.hi()


# Gradle #


## Install ##

	# 使用 gvm 安裝
	Linux:~ # gvm install gradle

	# 確認環境變數
	Linux:~ $ echo $JAVA_HOME
	Linux:~ $ echo $GRADLE_HOME

	# 測試
	Linux:~ $ cat build.gradle
	task hello {
	    println "Hello"
	}
	Linux:~ $ gradle -q hello

## Command ##

	Linux:~ $ gradle tasks
	Linux:~ $ gradle build
	Linux:~ $ gradle distZip