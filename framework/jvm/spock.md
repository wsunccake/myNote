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

## Basics

### Specification template

```groovy
class MyFirstSpecification extends Specification {
  // fields
  // fixture methods
  // feature methods
  // helper methods
}
```


### Blocks order

```groovy
    given:    //data initialization goes here (includes creating mocks)
    when:     //invoke your test subject here and assign it to a variable
    then:     //assert data here
    cleanup:  //optional
    where:    //optional:provide parametrized data (tables or pipes) 
```

or

```groovy
    given:
    expect:   //combines when with then
    cleanup: 
    where:
```


### Fixture Method

```groovy
ef setup() {}          // run before every feature method
def cleanup() {}        // run after every feature method
def setupSpec() {}     // run before the first feature method
def cleanupSpec() {}   // run after the last feature method
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

## Data Driven Testing

### Data Tables

```groovy
class Math extends Specification {
    def "maximum of two numbers"(int a, int b, int c) {
        expect:
        Math.max(a, b) == c

        where:
        a | b | c
        1 | 3 | 3   //passes
        7 | 4 | 4   //fails
        0 | 0 | 0   //passes
    }
}
```

=>

```groovy
        where:
        a | b || c
        1 | 3 || 3
        7 | 4 || 4
        0 | 0 || 0
```


### Unrolling

```groovy
@Unroll
def "maximum of two numbers"() { ... }
```

`with unroll`

```
maximum of two numbers[0]   PASSED
maximum of two numbers[1]   FAILED

Math.max(a, b) == c
    |    |  |  |  |
    |    7  0  |  7
    42         false
```

`without unroll`

```
maximum of two numbers   FAILED

Condition not satisfied:

Math.max(a, b) == c
    |    |  |  |  |
    |    7  0  |  7
    42         false
```

### Data Pipe

`variable`

```groovy
where:
a << [3, 7, 0]
b << [5, 0, 0]
c << [5, 7, 0]

[x, y, z] << sql.rows("select x, y, z from maxdata")
```

`multi variable`

```groovy
row << sql.rows("select * from maxdata")
a = row.a
b = row.b
```

`ignore variable`

```groovy
[a, b] << [[1,2,3],[1,2,3],[4,5,6]]
[a, b, _, c] << sql.rows("select * from maxdata")
```

`combine data table, pipe`

```groovy
where:
a | _
3 | _
7 | _
0 | _

b << [5, 0, 0]

c = a > b ? a : b
```

---

## Interaction Based Testing

### Mocking

```groovy
def "should send messages to all subscribers"() {
    // create mock
    Subscriber subscriber = Mock()
    def subscriber2 = Mock(Subscriber)

    when:
    publisher.send("hello")

    then:
    1 * subscriber.receive("hello") //subsriber should call receive with "hello" once.
    1 * subscriber2.receive("hello")
}
```


### Cardinality

```groovy
1 * subscriber.receive("hello")      // exactly one call
0 * subscriber.receive("hello")      // zero calls
(1..3) * subscriber.receive("hello") // between one and three calls (inclusive)
(1.._) * subscriber.receive("hello") // at least one call
(_..3) * subscriber.receive("hello") // at most three calls
_ * subscriber.receive("hello")      // any number of calls, including zero
                                     // (rarely needed; see 'Strict Mocking')
```


### Constraint

```groovy
// Target
1 * subscriber.receive("hello") // a call to 'subscriber'
1 * _.receive("hello")          // a call to any mock object

// Method
1 * subscriber.receive("hello") // a method named 'receive'
1 * subscriber./r.*e/("hello")  // a method whose name matches the given regular expression
                                // (here: method name starts with 'r' and ends in 'e')

// Argument
1 * subscriber.receive("hello")     // an argument that is equal to the String "hello"
1 * subscriber.receive(!"hello")    // an argument that is unequal to the String "hello"
1 * subscriber.receive()            // the empty argument list (would never match in our example)
1 * subscriber.receive(_)           // any single argument (including null)
1 * subscriber.receive(*_)          // any argument list (including the empty argument list)
1 * subscriber.receive(!null)       // any non-null argument
1 * subscriber.receive(_ as String) // any non-null argument that is-a String
1 * subscriber.receive({ it.size() > 3 }) // an argument that satisfies the given predicate
                                          // (here: message length is greater than 3)   
```


### Mock Creation

```groovy
class MySpec extends Specification {
    Subscriber subscriber = Mock {
        1 * receive("hello")
        1 * receive("goodbye")
    }
}
```


### Group Interaction

```groovy
with(mock) {
    1 * receive("hello")
    1 * receive("goodbye")
}
```

### Stubbing

```groovy
def subsriber = Stub(Subscriber)
...
subscriber.receive(_) >> "ok"
subscriber.receive(_) >>> ["ok", "error", "error", "ok"]
subscriber.receive(_) >>> ["ok", "fail", "ok"] >> { throw new InternalError() } >> "ok"
```


---

## Extension

```groovy
@Ignore(reason = "TODO")
@IgnoreRest
@IgnoreIf({ spock.util.environment.Jvm.isJava5()) })
@Requires({ os.windows })
@Timeout(5)
@Timeout(value = 100, unit = TimeUnit.MILLISECONDS)
@Title("This tests if..."
@Narrative("some detailed explanation")
@Issue("http://redmine/23432")
@Subject
```


---

## Reference

[Spock Framework Reference Documentation](http://spockframework.org/spock/docs/1.1/index.html)

[JUnit vs Spock + Spock Cheatsheet](http://jakubdziworski.github.io/java/groovy/spock/2016/05/14/spock-cheatsheet.html)
