# statement

## variable definition

```groovy
String x
def y
var z
```


## variable assignment

```groovy
x = 1
println x

x = new java.util.Date()
println x

x = -3.1499392
println x

x = false
println x

x = "Hi"
println x


// multiple assignment
def (a, b, c) = [10, 20, 'foo']
assert a == 10 && b == 20 && c == 'foo'

def (int i, String j) = [10, 'foo']
assert i == 10 && j == 'foo'

def nums = [1, 3, 5]
def a, b, c
(a, b, c) = nums
assert a == 1 && b == 3 && c == 5

def (_, month, year) = "18th June 2009".split()
assert "In $month of $year" == 'In June of 2009'


// overflow and underflow
def (a, b, c) = [1, 2]
assert a == 1 && b == 2 && c == null

def (a, b) = [1, 2, 3]
assert a == 1 && b == 2


// object destructuring with multiple assignment
@Immutable
class Coordinates {
    double latitude
    double longitude

    double getAt(int idx) {
        if (idx == 0) latitude
        else if (idx == 1) longitude
        else throw new Exception("Wrong coordinate index, use 0 or 1")
    }
}

def coordinates = new Coordinates(latitude: 43.23, longitude: 3.67)
def (la, lo) = coordinates

assert la == 43.23
assert lo == 3.67
```


## control structure

conditional structure

```groovy
// if / else
def x = false
def y = false

if ( !x ) {
    x = true
}
assert x == true

if ( x ) {
    x = false
} else {
    y = true
}
assert x == y

if ( ... ) {
    ...
} else if (...) {
    ...
} else {
    ...
}


// switch / case
def x = 1.23
def result = ""

switch (x) {
    case "foo":
        result = "found foo"
                        // lets fall through

    case "bar":
        result += "bar"

    case [4, 5, 6, 'inList']:
        result = "list"
        break

    case 12..30:
        result = "range"
        break

    case Integer:
        result = "integer"
        break

    case Number:
        result = "number"
        break

    case ~/fo*/:        // toString() representation of x matches the pattern?
        result = "foo regex"
        break

    case { it < 0 }:    // or { x < 0 }
        result = "negative"
        break

    default:
        result = "default"
}
assert result == "number"

def partner = switch(person) {
    case 'Romeo'  -> 'Juliet'
    case 'Adam'   -> 'Eve'
    case 'Antony' -> 'Cleopatra'
    case 'Bonnie' -> 'Clyde'
}
```

looping structure

```groovy
// classic for loop
String message = ''
for (int i = 0; i < 5; i++) {
    message += 'Hi '
}
assert message == 'Hi Hi Hi Hi Hi '


// enhanced classic java-style for loop
def facts = []
def count = 5
for (int fact = 1, i = 1; i <= count; i++, fact *= i) {
    facts << fact
}
assert facts == [1, 2, 6, 24, 120]


// multi-assignment in combination with for loop
// multi-assignment with types
def (String x, int y) = ['foo', 42]
assert "$x $y" == 'foo 42'

// multi-assignment goes loopy
def baNums = []
for (def (String u, int v) = ['bar', 42]; v < 45; u++, v++) {
    baNums << "$u $v"
}
assert baNums == ['bar 42', 'bas 43', 'bat 44']
```

for in loop

```groovy
// iterate over a range
def x = 0
for ( i in 0..9 ) {
    x += i
}
assert x == 45


// iterate over a list
x = 0
for ( i in [0, 1, 2, 3, 4] ) {
    x += i
}
assert x == 10


// iterate over an array
def array = (0..4).toArray()
x = 0
for ( i in array ) {
    x += i
}
assert x == 10

// iterate over a map
def map = ['abc':1, 'def':2, 'xyz':3]
x = 0
for ( e in map ) {
    x += e.value
}
assert x == 6


// iterate over values in a map
x = 0
for ( v in map.values() ) {
    x += v
}
assert x == 6


// iterate over the characters in a string
def text = "abc"
def list = []
for (c in text) {
    list.add(c)
}
assert list == ["a", "b", "c"]
```

while loop

```groovy
def x = 0
def y = 5

while ( y-- > 0 ) {
    x++
}

assert x == 5
```

do/while loop

```groovy
// classic Java-style do..while loop
def count = 5
def fact = 1
do {
    fact *= count--
} while(count > 1)
assert fact == 120
```

exception handling

try / catch / finally

```groovy
try {
    'moo'.toLong()   // this will generate an exception
    assert false     // asserting that this point should never be reached
} catch ( e ) {
    assert e in NumberFormatException
}


def z
try {
    def i = 7, j = 0
    try {
        def k = i / j
        assert false        //never reached due to Exception in previous line
    } finally {
        z = 'reached here'  //always executed even if Exception thrown
    }
} catch ( e ) {
    assert e in ArithmeticException
    assert z == 'reached here'
}
```

multi-catch

```groovy
try {
    /* ... */
} catch ( IOException | NullPointerException e ) {
    /* one block to handle 2 exceptions */
}
```

ARM try with resources

```groovy
class FromResource extends ByteArrayInputStream {
    @Override
    void close() throws IOException {
        super.close()
        println "FromResource closing"
    }

    FromResource(String input) {
        super(input.toLowerCase().bytes)
    }
}

class ToResource extends ByteArrayOutputStream {
    @Override
    void close() throws IOException {
        super.close()
        println "ToResource closing"
    }
}

def wrestle(s) {
    try (
            FromResource from = new FromResource(s)
            ToResource to = new ToResource()
    ) {
        to << from
        return to.toString()
    }
}

def wrestle2(s) {
    FromResource from = new FromResource(s)
    try (from; ToResource to = new ToResource()) { // Enhanced try-with-resources in Java 9+
        to << from
        return to.toString()
    }
}

assert wrestle("ARM was here!").contains('arm')
assert wrestle2("ARM was here!").contains('arm')
```


## power assertion

```groovy
assert [left expression] == [right expression] : (optional message)

assert 1+1 == 3

def x = 2
def y = 7
def z = 5
def calc = { a,b -> a*b+1 }
assert calc(x,y) == [x,z].sum()
assert calc(x,y) == z*z : 'Incorrect computation result'
```


## labeled statement

```groovy
given:
    def x = 1
    def y = 2
when:
    def z = x+y
then:
    assert z == 3


for (int i=0;i<10;i++) {
    for (int j=0;j<i;j++) {
        println "j=$j"
        if (j == 5) {
            break exit
        }
    }
    exit: println "i=$i"
}
```


---

# expression

## expression


## GPath expression

```groovy
// object navigation
void aMethodFoo() { println "This is aMethodFoo." }

assert ['aMethodFoo'] == this.class.methods.name.grep(~/.*Foo/)

void aMethodBar() { println "This is aMethodBar." }
void anotherFooMethod() { println "This is anotherFooMethod." }
void aSecondMethodBar() { println "This is aSecondMethodBar." }

assert ['aMethodBar', 'aSecondMethodBar'] as Set == this.class.methods.name.grep(~/.*Bar/) as Set


// expression deconstruction
List<String> methodNames = new ArrayList<String>();
for (Method method : this.getClass().getMethods()) {
   methodNames.add(method.getName());
}
return methodNames;

assert 'aSecondMethodBar' == this.class.methods.name.grep(~/.*Bar/).sort()[1]


// GPath for XML navigation
def xmlText = """
              | <root>
              |   <level>
              |      <sublevel id='1'>
              |        <keyVal>
              |          <key>mykey</key>
              |          <value>value 123</value>
              |        </keyVal>
              |      </sublevel>
              |      <sublevel id='2'>
              |        <keyVal>
              |          <key>anotherKey</key>
              |          <value>42</value>
              |        </keyVal>
              |        <keyVal>
              |          <key>mykey</key>
              |          <value>fizzbuzz</value>
              |        </keyVal>
              |      </sublevel>
              |   </level>
              | </root>
              """
def root = new XmlSlurper().parseText(xmlText.stripMargin())
assert root.level.size() == 1
assert root.level.sublevel.size() == 2
assert root.level.sublevel.findAll { it.@id == 1 }.size() == 1
assert root.level.sublevel[1].keyVal[0].key.text() == 'anotherKey'
```


---

# promotion and coercion

## closure to type coercion

```groovy
// assigning a closure to a SAM type
interface Predicate<T> {
    boolean accept(T obj)
}

abstract class Greeter {
    abstract String getName()
    void greet() {
        println "Hello, $name"
    }
}

// SAM type using the as operator
Predicate filter = { it.contains 'G' } as Predicate
assert filter.accept('Groovy') == true
Greeter greeter = { 'Groovy' } as Greeter
greeter.greet()

// as Type expression is optional since Groovy 2.2.0
Predicate filter = { it.contains 'G' }
assert filter.accept('Groovy') == true
Greeter greeter = { 'Groovy' }
greeter.greet()

boolean doFilter(String s) { s.contains('G') }
Predicate filter = this.&doFilter
assert filter.accept('Groovy') == true
Greeter greeter = GroovySystem.&getVersion
greeter.greet()


// calling a method accepting a SAM type with a closure
public <T> List<T> filter(List<T> source, Predicate<T> predicate) {
    source.findAll { predicate.accept(it) }
}
assert filter(['Java','Groovy'], { it.contains 'G'} as Predicate) == ['Groovy']
assert filter(['Java','Groovy']) { it.contains 'G'} == ['Groovy']


// closure to arbitrary type coercion
interface FooBar {
    int foo()
    void bar()
}
def impl = { println 'ok'; 123 } as FooBar
assert impl.foo() == 123
impl.bar()
// -->
class FooBar {
    int foo() { 1 }
    void bar() { println 'bar' }
}
def impl = { println 'ok'; 123 } as FooBar
assert impl.foo() == 123
impl.bar()
```


## map to type coercion

```groovy
def map
map = [
  i: 10,
  hasNext: { map.i > 0 },
  next: { map.i-- },
]
def iter = map as Iterator

interface X {
    void f()
    void g(int n)
    void h(String s, int n)
}

x = [ f: {println "f called"} ] as X
x.f()   // method exists
x.g()   // MissingMethodException here
x.g(5)  // UnsupportedOperationException here
```


## string to enum coercion

```groovy
enum State {
    up,
    down
}


State st = 'up'
assert st == State.up

def val = "up"
State st = "${val}"
assert st == State.up

State st = 'not an enum value'

State switchState(State st) {
    switch (st) {
        case 'up':
            return State.down // explicit constant
        case 'down':
            return 'up' // implicit coercion for return types
    }
}

assert switchState('up' as State) == State.down
assert switchState(State.down) == State.up
```


## custom type coercion

```groovy
class Polar {
    double r
    double phi
}
class Cartesian {
   double x
   double y
}

def asType(Class target) {
    if (Cartesian==target) {
        return new Cartesian(x: r*cos(phi), y: r*sin(phi))
    }
}

def sigma = 1E-16
def polar = new Polar(r:1.0,phi:PI/2)
def cartesian = polar as Cartesian
assert abs(cartesian.x-sigma) < sigma

// -->

class Polar {
    double r
    double phi
    def asType(Class target) {
        if (Cartesian==target) {
            return new Cartesian(x: r*cos(phi), y: r*sin(phi))
        }
    }
}

Polar.metaClass.asType = { Class target ->
    if (Cartesian==target) {
        return new Cartesian(x: r*cos(phi), y: r*sin(phi))
    }
}
```


## class literals vs variable and the as operator

```groovy
interface Greeter {
    void greet()
}
def greeter = { println 'Hello, Groovy!' } as Greeter // Greeter is known statically
greeter.greet()

Class clazz = Class.forName('Greeter')

greeter = { println 'Hello, Groovy!' } as clazz
// throws:
// unable to resolve class clazz
// @ line 9, column 40.
//   greeter = { println 'Hello, Groovy!' } as clazz

greeter = { println 'Hello, Groovy!' }.asType(clazz)
greeter.greet()
```


---

# optionality

## optional parenthes

```groovy
println 'Hello World'
def maximum = Math.max 5, 10
// -->
println()
println(Math.max(5, 10))
```


## optional semicolon

```groovy
assert true;
// -->
assert true

boolean a = true; assert a
```


## optional return keyword

```groovy
int add(int a, int b) {
    return a+b
}
assert add(1, 2) == 3
// -->
int add(int a, int b) {
    a+b
}
assert add(1, 2) == 3
```


## optional public keyword

```groovy
public class Server {
    public String toString() { "a server" }
}
// -->
class Server {
    String toString() { "a server" }
}
```


---

# the groovy truth

```groovy
// boolean expression
assert true
assert !false


// collection and array
assert [1, 2, 3]
assert ![]


// matcher
assert ('a' =~ /a/)
assert !('a' =~ /b/)


// iterator and enumeration
assert [0].iterator()
assert ![].iterator()
Vector v = [0] as Vector
Enumeration enumeration = v.elements()
assert enumeration
enumeration.nextElement()
assert !enumeration


// map
assert ['one' : 1]
assert ![:]


// string
assert 'a'
assert !''
def nonEmpty = 'a'
assert "$nonEmpty"
def empty = ''
assert !"$empty"


// number
assert 1
assert 3.5
assert !0


// object reference
assert new Object()
assert !null


// customizing the truth with asBoolean() method
class Color {
    String name

    boolean asBoolean(){
        name == 'green' ? true : false
    }
}
assert new Color(name: 'green')
assert !new Color(name: 'red')
```


---

# typing
