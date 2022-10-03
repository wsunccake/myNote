# groovy 4.x

## install

```bash
# require java
linux:~ # apt install openjdk-17-jdk | openjdk-11-jdk   ## for debian / ubuntu

# download groovy
linux:~ # curl -LO https://archive.apache.org/dist/groovy/4.0.5/distribution/apache-groovy-sdk-4.0.5.zip

# install groovy
linux:~ # unzip -d /usr/local apache-groovy-sdk-4.0.5.zip
linux:~ # ln -s /usr/local/groovy-4.0.5/bin/groovy /usr/local/bin

# test groovy
linux:~ # groovy -version
linux:~ # groovy -e 'println "Hello Groovy"
```


---

## run

```bash
# command mode
linux:~ $ groovy -e "println 'Hi, Groovy'"

# script mode
linux:~ $ cat hi.groovy
println 'Hi, Groovy'
linux:~ $ groovy hi.groovy

# inactive mode
linux:~ $ export EDITOR=vim
linux:~ $ groovysh
groovy> println 'Hi, Groovy'
groovy> :load hi.groovy
groovy> :edit
def abc() {
    println "abc"
}
groovy> abc
groovy> :show all
groovy> [].getClass()
groovy> :doc java.util.ArrayList
```
