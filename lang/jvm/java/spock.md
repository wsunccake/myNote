# Spock

## Hello

`project`

```bash
linux:~/project # gradle init
```

`gradle`

```bash
linux:~/project # vi build.gradle
plugins {
  id 'groovy'
  id 'java'
}

version '1.0-SNAPSHOT'

sourceCompatibility = 1.8

repositories {
  mavenCentral()
}

dependencies {
  compile 'org.codehaus.groovy:groovy-all:2.4.14'
  testCompile 'org.spockframework:spock-core:1.1-groovy-2.4'
}
```

`class`

```bash
linux:~/project # vi src/main/java/com/mycls/Hello.java 
package com.mycls;

public class Hello {
  public String say(String name) {
      return "Hello " + name;
  }
}
```

`test`

```bash
linux:~/project # vi src/test/groovy/com/mycls/HelloSpec.groovy
package com.mycls

import spock.lang.Specification

class HelloSpec extends Specification {
  def "say hello" () {
      when:
      Hello hello = new Hello()

      then:
      hello.say(name) == words

      where:
      name    | words
      'Spock' | 'Hello Spock'
      'Java'  | 'Hello Java'
      'Groovy'| 'Hello Groovy'
  }

  def "say hello with expect"() {
      expect:
      new Hello().say(name) == words

      where:
      name    | words
      'Spock' | 'Hello Spock'
      'Java'  | 'Hello Java'
      'Groovy'| 'Hello Groovy'
  }
}
```

`run`

```bash
linux:~/project # gradle clean test
```

---

## Primer

### Fixture Method

Fixture Methods	| Description
---				| ---
setup			| run before every feature method
cleanup			| run after every feature method
setupSpec 		| run before the first feature method
cleanupSpec 	| run after the last feature method

```groovy
def setup() {}
def cleanup() {}
def setupSpec() {}
def cleanupSpec() {}
```


### Feature method

```groovy
def "pushing an element on the stack"() {
  // blocks go here
}
```


### Helper Method

`origin`

```groovy
def "offered PC matches preferred configuration"() {
  when:
  def pc = shop.buyPc()

  then:
  pc.vendor == "Sunny"
  pc.clockRate >= 2333
  pc.ram >= 4096
  pc.os == "Linux"
}
```

`helper`

```groovy
def "offered PC matches preferred configuration"() {
  when:
  def pc = shop.buyPc()

  then:
  matchesPreferredConfiguration(pc)
}

def matchesPreferredConfiguration(pc) {
  assert pc.vendor == "Sunny"
  assert pc.clockRate >= 2333
  assert pc.ram >= 4096
  assert pc.os == "Linux"
}
```


---

## Reference

[Spock Framework Reference Documentation](http://spockframework.org/spock/docs/1.1/index.html)
