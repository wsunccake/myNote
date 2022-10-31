# type

```
Primitive type      Wrapper class
boolean             Boolean
char                Character
short               Short
int                 Integer
long                Long
float               Float
double              Double
```

```groovy
// primitive type
class Foo {
    static int i
}

assert Foo.class.getDeclaredField('i').type == int.class
assert Foo.i.class != int.class && Foo.i.class == Integer.class


// reference type
String movie = 'The Matrix'
List actors = ['Keanu Reeves', 'Hugo Weaving']


// generic
List<String> roles = ['Trinity', 'Morpheus']
```


---

# class

```groovy
// normal class

class Person {                          // class
    String name                         // field
    Integer age

    def increaseAge(Integer years) {    // method
        this.age += years
    }
}
def p = new Person()


// inner class
class Outer {
    private String privateStr = 'some string'

    def startThread() {
       new Thread(new Inner()).start()
    }

    class Inner implements Runnable {   // inner class
        void run() {
            println "${privateStr}."
        }
    }
}

class Computer {
    class Cpu {
        int coreNumber

        Cpu(int coreNumber) {
            this.coreNumber = coreNumber
        }
    }
}
assert 4 == new Computer().new Cpu(4).coreNumber    // java syntax for non-static inner class instantiation


// anonymous inner class
class Outer {
    private String privateStr = 'some string'

    def startThread() {
        new Thread(new Runnable() {
            void run() {
                println "${privateStr}."
            }
        }).start()
    }
}


// abstract class
abstract class Abstract {
    String name

    abstract def abstractMethod()

    def concreteMethod() {
        println 'concrete'
    }
}
```


---

## inheritance

superclass, traits, interface


---

## superclass

extends


---

## interface

```groovy
interface Greeter {
    void greet(String name)
}

// implements
class SystemGreeter implements Greeter {
    void greet(String name) {
        println "Hello $name"
    }
}
def greeter = new SystemGreeter()
assert greeter instanceof Greeter

// extends
interface ExtendedGreeter extends Greeter {
    void sayBye(String name)
}

// declare / define method
class DefaultGreeter {
    void greet(String name) { println "Hello" }
}
greeter = new DefaultGreeter()
assert !(greeter instanceof Greeter)

// implement interface
greeter = new DefaultGreeter()
coerced = greeter as Greeter
assert coerced instanceof Greeter
```


---

# class member

## constructor

```groovy
//  positional parameter
class PersonConstructor {
    String name
    Integer age

    PersonConstructor(name, age) {
        this.name = name
        this.age = age
    }
}
def person1 = new PersonConstructor('Marie', 1)
def person2 = ['Marie', 2] as PersonConstructor
PersonConstructor person3 = ['Marie', 3]


// named parameter
class PersonWOConstructor {
    String name
    Integer age
}
def person4 = new PersonWOConstructor()
def person5 = new PersonWOConstructor(name: 'Marie')
def person6 = new PersonWOConstructor(age: 1)
def person7 = new PersonWOConstructor(name: 'Marie', age: 2)
```


## method

```groovy
// method definition
def someMethod() { 'method called' }
String anotherMethod() { 'another method called' }
def thirdMethod(param1) { "$param1 passed" }
static String fourthMethod(String param1) { "$param1 passed" }


// named parameter
def foo(Map args) { "${args.name}: ${args.age}" }
foo(name: 'Marie', age: 1)


// mixing named and positional parameter
def foo(Map args, Integer number) { "${args.name}: ${args.age}, and the number is ${number}" }
foo(name: 'Marie', age: 1, 23)
foo(23, name: 'Marie', age: 1)

def foo(Integer number, Map args) { "${args.name}: ${args.age}, and the number is ${number}" }
foo(name: 'Marie', age: 1, 23)

def foo(Integer number, Map args) { "${args.name}: ${args.age}, and the number is ${number}" }
foo(23, [name: 'Marie', age: 1])


// default argument
def foo(String par1, Integer par2 = 1) { [name: par1, age: par2] }
assert foo('Marie').age == 1

def baz(a = 'a', int b, c = 'c', boolean d, e = 'e') { "$a $b $c $d $e" }

assert baz(42, true) == 'a 42 c true e'
assert baz('A', 42, true) == 'A 42 c true e'
assert baz('A', 42, 'C', true) == 'A 42 C true e'
assert baz('A', 42, 'C', true, 'E') == 'A 42 C true E'


// vararg
def foo(Object... args) { args.length }
assert foo() == 0
assert foo(1) == 1
assert foo(1, 2) == 2

def foo(Object[] args) { args.length }
assert foo() == 0
assert foo(1) == 1
assert foo(1, 2) == 2

def foo(Object... args) { args }
assert foo(null) == null

def foo(Object... args) { args }
Integer[] ints = [1, 2]
assert foo(ints) == [1, 2]

def foo(Object... args) { 1 }
def foo(Object x) { 2 }
assert foo() == 1
assert foo(1) == 2
assert foo(1, 2) == 1


// method selection algorithm
def method(Object o1, Object o2) { 'o/o' }
def method(Integer i, String  s) { 'i/s' }
def method(String  s, Integer i) { 's/i' }
assert method('foo', 42) == 's/i'
List<List<Object>> pairs = [['foo', 1], [2, 'bar'], [3, 4]]
assert pairs.collect { a, b -> method(a, b) } == ['s/i', 'i/s', 'o/o']

// directly implement interface
interface I1 {}
interface I2 extends I1 {}
interface I3 {}
class Clazz implements I3, I2 {}
def method(I1 i1) { 'I1' }
def method(I3 i3) { 'I3' }
assert method(new Clazz()) == 'I3'

// object array prefer over object
def method(Object[] arg) { 'array' }
def method(Object arg) { 'object' }
assert method([] as Object[]) == 'array'

// non-vararg variant
def method(String s, Object... vargs) { 'vararg' }
def method(String s) { 'non-vararg' }
assert method('foo') == 'non-vararg'

// minimum number of vararg arguments prefer
def method(String s, Object... vargs) { 'two vargs' }
def method(String s, Integer i, Object... vargs) { 'one varg' }
assert method('foo', 35, new Date()) == 'one varg'

// interface prefer over super class
interface I {}
class Base {}
class Child extends Base implements I {}
def method(Base b) { 'superclass' }
def method(I i) { 'interface' }
assert method(new Child()) == 'interface'

// slightly larger prefer
def method(Long l) { 'Long' }
def method(Short s) { 'Short' }
def method(BigInteger bi) { 'BigInteger' }
assert method(35) == 'Long'

def method(Date d, Object o) { 'd/o' }
def method(Object o, String s) { 'o/s' }
def ex = shouldFail {
    println method(new Date(), 'baz')
}
assert ex.message.contains('Ambiguous method overloading')
assert method(new Date(), (Object)'baz') == 'd/o'
assert method((Object)new Date(), 'baz') == 'o/s'


// exception declaration
def badRead() {
    new File('doesNotExist.txt').text
}

shouldFail(FileNotFoundException) {
    badRead()
}
```


---

# field and property

field: no getter / setter

property: with getter / setter


## field

```groovy
class Data {
    private int id
    protected String description
    public static final boolean DEBUG = false
}

class Data {
    private String id = IDGenerator.next()
    // ...
}

class BadPractice {
    private mapping
}

class GoodPractice {
    private Map<String,String> mapping
}
```


## property

```groovy
class Person {
    String name
    int age
}

class Person {
    final String name       // final -> no setter
    final int age
    Person(String name, int age) {
        this.name = name
        this.age = age
    }
}

class Person {
    String name
    void name(String name) {
        this.name = "Wonder $name"
    }
    String title() {
        this.name
    }
}
def p = new Person()
p.name = 'Diana'
assert p.name == 'Diana'
p.name('Woman')
assert p.title() == 'Wonder Woman'

class Person {
    String name
    int age
}
def p = new Person()
assert p.properties.keySet().containsAll(['name','age'])

class PseudoProperties {
    // a pseudo property "name"
    void setName(String name) {}
    String getName() {}

    // a pseudo read-only property "age"
    int getAge() { 42 }

    // a pseudo write-only property "groovy"
    void setGroovy(boolean groovy) {  }
}
def p = new PseudoProperties()
p.name = 'Foo'
assert p.age == 42
p.groovy = true

// annotations on a property
class Animal {
    int lowerCount = 0
    @Lazy String name = { lower().toUpperCase() }()
    String lower() { lowerCount++; 'sloth' }
}
def a = new Animal()
assert a.lowerCount == 0
assert a.name == 'SLOTH'
assert a.lowerCount == 1

// split property definition with an explicit backing field
class HasPropertyWithProtectedField {
    protected String name
    String name
}

class HasPropertyWithPackagePrivateField {
    String name
    @PackageScope String name
}

class HasPropertyWithSynchronizedAccessorMethods {
    private String name
    @Synchronized String name
}
```

```groovy
class Person {
    String name
    void name(String name) {
        this.name = "Wonder $name"
    }
    String title() {
        this.name
    }
}

Person.metaClass.getProperties().findAll {
    println(it.name)
}

Person.metaClass.methods.findAll {
    println(it.name)
}

def m = Person.declaredMethods.findAll {
    !it.synthetic && !it.getAnnotation(groovy.transform.Internal)
}.name
println(m)
```

---

#  annotation

```groovy
// marker annotation
@interface MarkerAnnotation {}


// single value annotation
@interface SingleValueAnnotation {
    String value()
}


// multi value annotation
@interface MultiValueAnnotation {
    String value()
    int number()
}
```

```groovy
// annotation definition
@interface SomeAnnotation {
    String value()
}
@interface SomeAnnotation {
    String value() default 'something'
}
@interface SomeAnnotation {
    int step()
}
@interface SomeAnnotation {
    Class appliesTo()
}
@interface SomeAnnotation {}
@interface SomeAnnotations {
    SomeAnnotation[] value()
}
enum DayOfWeek { mon, tue, wed, thu, fri, sat, sun }
@interface Scheduled {
    DayOfWeek dayOfWeek()
}


//  annotation placement
@SomeAnnotation
void someMethod() {
    // ...
}

@SomeAnnotation
class SomeClass {}

@SomeAnnotation String var


// Target
import java.lang.annotation.ElementType
import java.lang.annotation.Target

@Target([ElementType.METHOD, ElementType.TYPE])
@interface SomeAnnotation {}


// Retention
import java.lang.annotation.Retention
import java.lang.annotation.RetentionPolicy

@Retention(RetentionPolicy.SOURCE)
@interface SomeAnnotation {}


// single value annotation
@interface Page {
    int statusCode()
}

@Page(statusCode=404)
void notFound() {
    // ...
}


// multi value annotation
@interface Page {
    String value()
    int statusCode() default 200
}

@Page(value='/home')
void home() {
    // ...
}

@Page('/users')
void userList() {
    // ...
}

@Page(value='error',statusCode=404)
void notFound() {
    // ...
}
```


---

# trait

```groovy
trait FlyingAbility {
        String fly() { "I'm flying!" }
}

class Bird implements FlyingAbility {}
def b = new Bird()
assert b.fly() == "I'm flying!"
```


## method

```groovy
// public method
trait FlyingAbility {
    String fly() { "I'm flying!" }
}


// abstract method
trait Greetable {
    abstract String name()
    String greeting() { "Hello, ${name()}!" }
}

class Person implements Greetable {
    String name() { 'Bob' }
}

def p = new Person()
assert p.greeting() == 'Hello, Bob!'


// private method
trait Greeter {
    private String greetingMessage() {
        'Hello from a private method!'
    }
    String greet() {
        def m = greetingMessage()
        println m
        m
    }
}
class GreetingMachine implements Greeter {}
def g = new GreetingMachine()
assert g.greet() == "Hello from a private method!"
try {
    assert g.greetingMessage()
} catch (MissingMethodException e) {
    println "greetingMessage is private in trait"
}
```


## this

```groovy
trait Introspector {
    def whoAmI() { this }
}
class Foo implements Introspector {}
def foo = new Foo()

assert foo.whoAmI().is(foo)
```


## interface

```groovy
interface Named {
    String name()
}
trait Greetable implements Named {
    String greeting() { "Hello, ${name()}!" }
}
class Person implements Greetable {
    String name() { 'Bob' }
}

def p = new Person()
assert p.greeting() == 'Hello, Bob!'
assert p instanceof Named
assert p instanceof Greetable
```


## property

```groovy
trait Named {
    String name
}
class Person implements Named {}
def p = new Person(name: 'Bob')
assert p.name == 'Bob'
assert p.getName() == 'Bob'
```


## field

```groovy
// private field
trait Counter {
    private int count = 0
    int count() { count += 1; count }
}
class Foo implements Counter {}
def f = new Foo()
assert f.count() == 1
assert f.count() == 2


// public field
trait Named {
    public String name
}
class Person implements Named {}
def p = new Person()
p.Named__name = 'Bob'
```


## composition

```groovy
trait FlyingAbility {
        String fly() { "I'm flying!" }
}
trait SpeakingAbility {
    String speak() { "I'm speaking!" }
}

class Duck implements FlyingAbility, SpeakingAbility {}

def d = new Duck()
assert d.fly() == "I'm flying!"
assert d.speak() == "I'm speaking!"
```


## overriding default method

```groovy
class Duck implements FlyingAbility, SpeakingAbility {
    String quack() { "Quack!" }
    String speak() { quack() }
}

def d = new Duck()
assert d.fly() == "I'm flying!"
assert d.quack() == "Quack!"
assert d.speak() == "Quack!"
```


## extending trait

```groovy
// simple inheritance
trait Named {
    String name
}
trait Polite extends Named {
    String introduce() { "Hello, I am $name" }
}
class Person implements Polite {}
def p = new Person(name: 'Alice')
assert p.introduce() == 'Hello, I am Alice'


// multiple inheritance
trait WithId {
    Long id
}
trait WithName {
    String name
}
trait Identified implements WithId, WithName {}
```


## duck typing and trait

```groovy
// dynamic code
trait SpeakingDuck {
    String speak() { quack() }
}
class Duck implements SpeakingDuck {
    String methodMissing(String name, args) {
        "${name.capitalize()}!"
    }
}
def d = new Duck()
assert d.speak() == 'Quack!'


// dynamic method in a trait
trait DynamicObject {
    private Map props = [:]
    def methodMissing(String name, args) {
        name.toUpperCase()
    }
    def propertyMissing(String name) {
        props.get(name)
    }
    void setProperty(String name, Object value) {
        props.put(name, value)
    }
}

class Dynamic implements DynamicObject {
    String existingProperty = 'ok'
    String existingMethod() { 'ok' }
}
def d = new Dynamic()
assert d.existingProperty == 'ok'
assert d.foo == null
d.foo = 'bar'
assert d.foo == 'bar'
assert d.existingMethod() == 'ok'
assert d.someMethod() == 'SOMEMETHOD'
```


## multiple inheritance conflict

```groovy
// default conflict resolution
trait A {
    String exec() { 'A' }
}
trait B {
    String exec() { 'B' }
}
class C implements A,B {}


// user conflict resolution
class C implements A,B {
    String exec() { A.super.exec() }
}
def c = new C()
assert c.exec() == 'A'
```


## runtime implementation of trait

```groovy
// implementing a trait at runtime
trait Extra {
    String extra() { "I'm an extra method" }
}
class Something {
    String doSomething() { 'Something' }
}
// def s = new Something()
// s.extra()
def s = new Something() as Extra
s.extra()
s.doSomething()


// implementing multiple traits at once
trait A { void methodFromA() {} }
trait B { void methodFromB() {} }
class C {}
def c = new C()
c.methodFromA()
c.methodFromB()
def d = c.withTraits A, B
d.methodFromA()
d.methodFromB()
```


## chaining behavior

```groovy
interface MessageHandler {
    void on(String message, Map payload)
}

trait DefaultHandler implements MessageHandler {
    void on(String message, Map payload) {
        println "Received $message with payload $payload"
    }
}

class SimpleHandler implements DefaultHandler {}

class SimpleHandlerWithLogging implements DefaultHandler {
    void on(String message, Map payload) {
        println "Seeing $message with payload $payload"
        DefaultHandler.super.on(message, payload)
    }
}

trait LoggingHandler implements MessageHandler {
    void on(String message, Map payload) {
        println "Seeing $message with payload $payload"
        super.on(message, payload)
    }
}

class HandlerWithLogger implements DefaultHandler, LoggingHandler {}
def loggingHandler = new HandlerWithLogger()
loggingHandler.on('test logging', [:])

trait SayHandler implements MessageHandler {
    void on(String message, Map payload) {
        if (message.startsWith("say")) {
            println "I say ${message - 'say'}!"
        } else {
            super.on(message, payload)
        }
    }
}

class Handler implements DefaultHandler, SayHandler, LoggingHandler {}
def h = new Handler()
h.on('foo', [:])
h.on('sayHello', [:])

class AlternateHandler implements DefaultHandler, LoggingHandler, SayHandler {}
h = new AlternateHandler()
h.on('foo', [:])
h.on('sayHello', [:])
```

```groovy
// semantic of super inside a trait
trait Filtering {
    StringBuilder append(String str) {
        def subst = str.replace('o','')
        super.append(subst)
    }
    String toString() { super.toString() }
}
def sb = new StringBuilder().withTraits Filtering
sb.append('Groovy')
assert sb.toString() == 'Grvy'
```


## advanced feature

```groovy
// SAM type coercion (Single Abstract Method)
trait Greeter {
    String greet() { "Hello $name" }
    abstract String getName()
}

Greeter greeter = { 'Alice' }

void greet(Greeter g) { println g.greet() }
greet { 'Alice' }
```

```groovy
// difference with Java 8 default method
import groovy.test.GroovyTestCase
import groovy.transform.CompileStatic
import org.codehaus.groovy.control.CompilerConfiguration
import org.codehaus.groovy.control.customizers.ASTTransformationCustomizer
import org.codehaus.groovy.control.customizers.ImportCustomizer

class SomeTest extends GroovyTestCase {
    def config
    def shell

    void setup() {
        config = new CompilerConfiguration()
        shell = new GroovyShell(config)
    }
    void testSomething() {
        assert shell.evaluate('1+1') == 2
    }
    void otherTest() { /* ... */ }
}

class AnotherTest extends SomeTest {
    void setup() {
        config = new CompilerConfiguration()
        config.addCompilationCustomizers( ... )
        shell = new GroovyShell(config)
    }
}

class YetAnotherTest extends SomeTest {
    void setup() {
        config = new CompilerConfiguration()
        config.addCompilationCustomizers( ... )
        shell = new GroovyShell(config)
    }
}

trait MyTestSupport {
    void setup() {
        config = new CompilerConfiguration()
        config.addCompilationCustomizers( new ASTTransformationCustomizer(CompileStatic) )
        shell = new GroovyShell(config)
    }
}

class AnotherTest extends SomeTest implements MyTestSupport {}
class YetAnotherTest extends SomeTest2 implements MyTestSupport {}

class Person {
    String name
}
trait Bob {
    String getName() { 'Bob' }
}

def p = new Person(name: 'Alice')
assert p.name == 'Alice'
def p2 = p as Bob
assert p2.name == 'Bob'
```


## differences with mixin

```groovy
class A { String methodFromA() { 'A' } }
class B { String methodFromB() { 'B' } }
A.metaClass.mixin B
def o = new A()
assert o.methodFromA() == 'A'
assert o.methodFromB() == 'B'
assert o instanceof A
assert !(o instanceof B)
```


## static method, property and field

```groovy
trait TestHelper {
    public static boolean CALLED = false
    static void init() {
        CALLED = true
    }
}
class Foo implements TestHelper {}
Foo.init()
assert Foo.TestHelper__CALLED


class Bar implements TestHelper {}
class Baz implements TestHelper {}
Bar.init()
assert Bar.TestHelper__CALLED
assert !Baz.TestHelper__CALLED
```


## inheritance of state gotchas

```groovy
trait IntCouple {
    int x = 1
    int y = 2
    int sum() { x+y }
}

class BaseElem implements IntCouple {
    int f() { sum() }
}
def base = new BaseElem()
assert base.f() == 3

class Elem implements IntCouple {
    int x = 3
    int y = 4
    int f() { sum() }
}
def elem = new Elem()
assert elem.f() == 3
```

```groovy
trait IntCouple {
    int x = 1
    int y = 2
    int sum() { getX()+getY() }
}

class Elem implements IntCouple {
    int x = 3
    int y = 4
    int f() { sum() }
}
def elem = new Elem()
assert elem.f() == 7
```


## self type

```groovy
// type constraint on trait
class CommunicationService {
    static void sendMessage(String from, String to, String message) {
        println "$from sent [$message] to $to"
    }
}

class Device { String id }

trait Communicating {
    void sendMessage(Device to, String message) {
        CommunicationService.sendMessage(id, to.id, message)
    }
}

class MyDevice extends Device implements Communicating {}

def bob = new MyDevice(id:'Bob')
def alice = new MyDevice(id:'Alice')
bob.sendMessage(alice,'secret')

class SecurityService {
    static void check(Device d) { if (d.id==null) throw new SecurityException() }
}


// @SelfType annotation
@SelfType(Device)
@CompileStatic
trait Communicating {
    void sendMessage(Device to, String message) {
        SecurityService.check(this)
        CommunicationService.sendMessage(id, to.id, message)
    }
}

class MyDevice implements Communicating {} // forgot to extend Device


// difference with sealed annotation (incubating)
interface HasHeight { double getHeight() }
interface HasArea { double getArea() }

@SelfType([HasHeight, HasArea])
@Sealed(permittedSubclasses=[UnitCylinder,UnitCube])
trait HasVolume {
    double getVolume() { height * area }
}

final class UnitCube implements HasVolume, HasHeight, HasArea {
    // for the purposes of this example: h=1, w=1, l=1
    double height = 1d
    double area = 1d
}

final class UnitCylinder implements HasVolume, HasHeight, HasArea {
    // for the purposes of this example: h=1, diameter=1
    // radius=diameter/2, area=PI * r^2
    double height = 1d
    double area = Math.PI * 0.5d**2
}

assert new UnitCube().volume == 1d
assert new UnitCylinder().volume == 0.7853981633974483d
```


## limitation

```groovy
// compatibility with AST transformation
@CompileStatic


// prefix and postfix operation
trait Counting {
    int x
    void inc() {
        x++
    }
    void dec() {
        --x
    }
}
class Counter implements Counting {}
def c = new Counter()
c.inc()
```


---

# record class (incubating)

```groovy
record Message(String from, String to, String body) { }

def msg = new Message('me@myhost.com', 'you@yourhost.net', 'Hello!')
assert msg.toString() == 'Message[from=me@myhost.com, to=you@yourhost.net, body=Hello!]'

// -->

final class Message extends Record {
    private final String from
    private final String to
    private final String body
    private static final long serialVersionUID = 0

    /* constructor(s) */

    final String toString() { /*...*/ }
    final boolean equals(Object other) { /*...*/ }
    final int hashCode() { /*...*/ }

    String from() { from }
    // other getters ...
}



// like JavaBean
record Point3D(int x, int y, int z) {
    String toString() {
        "Point3D[coords=$x,$y,$z]"
    }
}
assert new Point3D(10, 20, 30).toString() == 'Point3D[coords=10,20,30]'

record Coord<T extends Number>(T v1, T v2){
    double distFromOrigin() { Math.sqrt(v1()**2 + v2()**2 as double) }
}
def r1 = new Coord<Integer>(3, 4)
assert r1.distFromOrigin() == 5
def r2 = new Coord<Double>(6d, 2.5d)
assert r2.distFromOrigin() == 6.5d
```


## special record feature

```groovy
// compact constructor
public record Warning(String message) {
    public Warning {
        Objects.requireNonNull(message)
        message = message.toUpperCase()
    }
}

def w = new Warning('Help')
assert w.message() == 'HELP'

// serializability
```


## groovy enhancement

```groovy
// argument default
record ColoredPoint(int x, int y = 0, String color = 'white') {}
assert new ColoredPoint(5, 5, 'black').toString() == 'ColoredPoint[x=5, y=5, color=black]'
assert new ColoredPoint(5, 5).toString() == 'ColoredPoint[x=5, y=5, color=white]'
assert new ColoredPoint(5).toString() == 'ColoredPoint[x=5, y=0, color=white]'

// -->

ColoredPoint(int, int, String)
ColoredPoint(int, int)
ColoredPoint(int)

assert new ColoredPoint(x: 5).toString() == 'ColoredPoint[x=5, y=0, color=white]'
assert new ColoredPoint(x: 0, y: 5).toString() == 'ColoredPoint[x=0, y=5, color=white]'


// default mode
@TupleConstructor(defaultsMode=DefaultsMode.OFF)
record ColoredPoint2(int x, int y, String color) {}
assert new ColoredPoint2(4, 5, 'red').toString() == 'ColoredPoint2[x=4, y=5, color=red]'

@TupleConstructor(defaultsMode=DefaultsMode.ON)
record ColoredPoint3(int x, int y = 0, String color = 'white') {}
assert new ColoredPoint3(y: 5).toString() == 'ColoredPoint3[x=0, y=5, color=white]'


// diving deeper
@RecordType
class Message {
    String from
    String to
    String body
}


// declarative toString customization
package threed

import groovy.transform.ToString

@ToString(ignoreNulls=true, cache=true, includeNames=true,
          leftDelimiter='[', rightDelimiter=']', nameValueSeparator='=')
record Point(Integer x, Integer y, Integer z=null) { }

assert new Point(10, 20).toString() == 'threed.Point[x=10, y=20]'


package twod

import groovy.transform.ToString

@ToString(ignoreNulls=true, cache=true, includeNames=true,
          leftDelimiter='[', rightDelimiter=']', nameValueSeparator='=')
record Point(Integer x, Integer y) { }

assert new Point(10, 20).toString() == 'twod.Point[x=10, y=20]'


// obtaining a list of the record component value
record Point(int x, int y, String color) { }

def p = new Point(100, 200, 'green')
def (x, y, c) = p.toList()
assert x == 100
assert y == 200
assert c == 'green'


// obtaining a map of the record component value
record Point(int x, int y, String color) { }

def p = new Point(100, 200, 'green')
assert p.toMap() == [x: 100, y: 200, color: 'green']


// obtaining the number of components in a record
record Point(int x, int y, String color) { }

def p = new Point(100, 200, 'green')
assert p.size() == 3


// obtaining the nth component from a record
record Point(int x, int y, String color) { }

def p = new Point(100, 200, 'green')
assert p[1] == 200
```


## optional groovy feature

```groovy
// coping
@RecordOptions(copyWith=true)
record Fruit(String name, double price) {}
def apple = new Fruit('Apple', 11.6)
assert 'Apple' == apple.name()
assert 11.6 == apple.price()

def orange = apple.copyWith(name: 'Orange')
assert orange.toString() == 'Fruit[name=Orange, price=11.6]'


// deep immutability
@ImmutableProperties
record Shopping(List items) {}

def items = ['bread', 'milk']
def shop = new Shopping(items)
items << 'chocolate'
assert shop.items() == ['bread', 'milk']


// obtaining the components of a record as a typed tuple
import groovy.transform.*

@RecordOptions(components=true)
record Point(int x, int y, String color) { }

@CompileStatic
def method() {
    def p1 = new Point(100, 200, 'green')
    def (int x1, int y1, String c1) = p1.components()
    assert x1 == 100
    assert y1 == 200
    assert c1 == 'green'

    def p2 = new Point(10, 20, 'blue')
    def (x2, y2, c2) = p2.components()
    assert x2 * 10 == 100
    assert y2 ** 2 == 400
    assert c2.toUpperCase() == 'BLUE'

    def p3 = new Point(1, 2, 'red')
    assert p3.components() instanceof Tuple3
}

method()
```


## other differences to java


## sealed hierarchy (incubating)

```groovy
//
sealed interface ShapeI permits Circle,Square { }
final class Circle implements ShapeI { }
final class Square implements ShapeI { }


//
@Sealed(permittedSubclasses=[Circle,Square]) interface ShapeI { }
final class Circle implements ShapeI { }
final class Square implements ShapeI { }


//
sealed class Shape permits Circle,Polygon,Rectangle { }

final class Circle extends Shape { }

class Polygon extends Shape { }
non-sealed class RegularPolygon extends Polygon { }
final class Hexagon extends Polygon { }

sealed class Rectangle extends Shape permits Square{ }
final class Square extends Rectangle { }```


//
enum Weather { Rainy, Cloudy, Sunny }
def forecast = [Weather.Rainy, Weather.Sunny, Weather.Cloudy]
assert forecast.toString() == '[Rainy, Sunny, Cloudy]'

sealed abstract class Weather { }
@Immutable(includeNames=true) class Rainy extends Weather { Integer expectedRainfall }
@Immutable(includeNames=true) class Sunny extends Weather { Integer expectedTemp }
@Immutable(includeNames=true) class Cloudy extends Weather { Integer expectedUV }
def forecast = [new Rainy(12), new Sunny(35), new Cloudy(6)]
assert forecast.toString() == '[Rainy(expectedRainfall:12), Sunny(expectedTemp:35), Cloudy(expectedUV:6)]'


//
import groovy.transform.*

sealed interface Tree<T> {}
@Singleton final class Empty implements Tree {
    String toString() { 'Empty' }
}
@Canonical final class Node<T> implements Tree<T> {
    T value
    Tree<T> left, right
}

Tree<Integer> tree = new Node<>(42, new Node<>(0, Empty.instance, Empty.instance), Empty.instance)
assert tree.toString() == 'Node(42, Node(0, Empty, Empty), Empty)'

sealed interface Expr {}
record ConstExpr(int i) implements Expr {}
record PlusExpr(Expr e1, Expr e2) implements Expr {}
record MinusExpr(Expr e1, Expr e2) implements Expr {}
record NegExpr(Expr e) implements Expr {}

def threePlusNegOne = new PlusExpr(new ConstExpr(3), new NegExpr(new ConstExpr(1)))
assert threePlusNegOne.toString() == 'PlusExpr[e1=ConstExpr[i=3], e2=NegExpr[e=ConstExpr[i=1]]]'
```


## difference to java
