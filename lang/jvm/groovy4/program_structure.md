# package

```bash
linux:~ $ mkdir -p com/my
linux:~ $ cat Tool.groovy
package com.my

class Tool {
    def hello() {
        println("Hello World")
    }
}

linux:~ $ cat main.groovy
import com.my.Tool

t = new Tool()
t.hello()

linux:~ $ groovy main.groovy
```


---

# import

```groovy
import groovy.json.JsonSlurper

def json_str = '''{
   "name": "Foo Bar",
   "year": 2020,
   "tags": [ "person", "employee" ],
   "grade": 3.14 }'''
def jsonSlurper = new JsonSlurper()
cfg = jsonSlurper.parseText(json_str)
println(cfg)
println(cfg['name'])
println(cfg.name)
```

```groovy
// default
import java.lang.*
import java.util.*
import java.io.*
import java.net.*
import groovy.lang.*
import groovy.util.*
import java.math.BigInteger
import java.math.BigDecimal


// simple import
import groovy.json.JsonSlurper


// star import
import groovy.json.*


// static import
import static com.my.Tool.hello


// import alias
import static com.my.Tool.hello as hi
```


---

# class versus script

## class

```groovy
// Main.groovy

class Main {
    static void main(String... args) {
        println 'Hello Groovy'
    }
}
```


## script

```groovy
// Main.groovy
import org.codehaus.groovy.runtime.InvokerHelper

class Main extends Script {
    def run() {
        println 'Hello Groovy'
    }

    static void main(String[] args) {
        InvokerHelper.runScript(Main, args)
    }
}
```