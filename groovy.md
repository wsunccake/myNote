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

`Hello1.groovy`

	public class Hello1 {
		public static void main(String[] args) {
			for(int i =0; i < 3; i++) {
				System.out.println("i = " + i);
			}
		}
	}

`Hello2.groovy`

	for(int i = 0; i < 3; i++) {
		System.out.println("i = " + i);
	}

`Hello3.groovy`

	for(i in 0..2) {
		println("i = " + i)
	}

`Hello4.groovy`

	0.upto(2) { println "i = ${it}" }
	3.times { println "i = $it" }

`Execute.groovy`

	println "groovy -v".execute().text


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