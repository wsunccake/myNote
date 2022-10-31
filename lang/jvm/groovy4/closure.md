# syntax

```groovy
// defining a closure
{ [closureParameters -> ] statements }


{ item++ }
{ -> item++ }
{ println it }
{ it -> println it }
{ name -> println name }
{ String x, int y ->
    println "hey ${x} the value is ${y}"
}
{ reader ->
    def line = reader.readLine()
    line.trim()
}


// closure as an object
def listener = { e -> println "Clicked on $e.source" }
assert listener instanceof Closure
Closure callback = { println 'Done!' }
Closure<Boolean> isTextFile = {
    File it -> it.name.endsWith('.txt')
}


// calling a closure
def code = { 123 }
assert code() == 123
assert code.call() == 123

def isOdd = { int i -> i%2 != 0 }
assert isOdd(3) == true
assert isOdd.call(2) == false

def isEven = { it%2 == 0 }
assert isEven(3) == false
assert isEven.call(2) == true
```


## parameter

```groovy
// normal parameter
def closureWithOneArg = { str -> str.toUpperCase() }
assert closureWithOneArg('groovy') == 'GROOVY'

def closureWithOneArgAndExplicitType = { String str -> str.toUpperCase() }
assert closureWithOneArgAndExplicitType('groovy') == 'GROOVY'

def closureWithTwoArgs = { a,b -> a+b }
assert closureWithTwoArgs(1,2) == 3

def closureWithTwoArgsAndExplicitTypes = { int a, int b -> a+b }
assert closureWithTwoArgsAndExplicitTypes(1,2) == 3

def closureWithTwoArgsAndOptionalTypes = { a, int b -> a+b }
assert closureWithTwoArgsAndOptionalTypes(1,2) == 3

def closureWithTwoArgAndDefaultValue = { int a, int b=2 -> a+b }
assert closureWithTwoArgAndDefaultValue(1) == 3


// implicit parameter
def greeting = { "Hello, $it!" }
assert greeting('Patrick') == 'Hello, Patrick!'

def greeting = { it -> "Hello, $it!" }
assert greeting('Patrick') == 'Hello, Patrick!'

def magicNumber = { -> 42 }
magicNumber(11)     // this call will fail because the closure doesn't accept any argument


// vararg
def concat1 = { String... args -> args.join('') }
assert concat1('abc','def') == 'abcdef'
def concat2 = { String[] args -> args.join('') }
assert concat2('abc', 'def') == 'abcdef'

def multiConcat = { int n, String... args ->
    args.join('')*n
}
assert multiConcat(2, 'abc','def') == 'abcdefabcdef'
```


## delegation strategy

```groovy
// groovy closure vs lambda expression

// groovy closure
{5}
{x -> 2 * x}
{x, y -> x - y}

// lambda expression
() -> 5
x -> 2 * x
(x, y) -> x – y
(int x, int y) -> x + y
(String s) -> System.out.print(s)
```


## owner, delegate and this

```groovy
// the meaning of this
class Enclosing {
    void run() {
        def whatIsThisObject = { getThisObject() }
        assert whatIsThisObject() == this
        def whatIsThis = { this }
        assert whatIsThis() == this
    }
}
class EnclosedInInnerClass {
    class Inner {
        Closure cl = { this }
    }
    void run() {
        def inner = new Inner()
        assert inner.cl() == inner
    }
}
class NestedClosures {
    void run() {
        def nestedClosures = {
            def cl = { this }
            cl()
        }
        assert nestedClosures() == this
    }
}

class Person {
    String name
    int age
    String toString() { "$name is $age years old" }

    String dump() {
        def cl = {
            String msg = this.toString()
            println msg
            msg
        }
        cl()
    }
}
def p = new Person(name:'Janice', age:74)
assert p.dump() == 'Janice is 74 years old'


// owner of a closure
class Enclosing {
    void run() {
        def whatIsOwnerMethod = { getOwner() }
        assert whatIsOwnerMethod() == this
        def whatIsOwner = { owner }
        assert whatIsOwner() == this
    }
}
class EnclosedInInnerClass {
    class Inner {
        Closure cl = { owner }
    }
    void run() {
        def inner = new Inner()
        assert inner.cl() == inner
    }
}
class NestedClosures {
    void run() {
        def nestedClosures = {
            def cl = { owner }
            cl()
        }
        assert nestedClosures() == nestedClosures
    }
}


// delegate of a closure
class Enclosing {
    void run() {
        def cl = { getDelegate() }
        def cl2 = { delegate }
        assert cl() == cl2()
        assert cl() == this
        def enclosed = {
            { -> delegate }.call()
        }
        assert enclosed() == enclosed
    }
}

class Person {
    String name
}
class Thing {
    String name
}
def p = new Person(name: 'Norman')
def t = new Thing(name: 'Teapot')

def upperCasedName = { delegate.name.toUpperCase() }
upperCasedName.delegate = p
assert upperCasedName() == 'NORMAN'
upperCasedName.delegate = t
assert upperCasedName() == 'TEAPOT'

def target = p
def upperCasedNameUsingVar = { target.name.toUpperCase() }
assert upperCasedNameUsingVar() == 'NORMAN'


// delegation strategy
class Person {
    String name
}
def p = new Person(name:'Igor')
def cl = { name.toUpperCase() }
cl.delegate = p
assert cl() == 'IGOR'

class Person {
    String name
    def pretty = { "My name is $name" }
    String toString() {
        pretty()
    }
}
class Thing {
    String name
}
def p = new Person(name: 'Sarah')
def t = new Thing(name: 'Teapot')
assert p.toString() == 'My name is Sarah'
p.pretty.delegate = t
assert p.toString() == 'My name is Sarah'

p.pretty.resolveStrategy = Closure.DELEGATE_FIRST
assert p.toString() == 'My name is Teapot'

class Person {
    String name
    int age
    def fetchAge = { age }
}
class Thing {
    String name
}

def p = new Person(name:'Jessica', age:42)
def t = new Thing(name:'Printer')
def cl = p.fetchAge
cl.delegate = p
assert cl() == 42
cl.delegate = t
assert cl() == 42
cl.resolveStrategy = Closure.DELEGATE_ONLY
cl.delegate = p
assert cl() == 42
cl.delegate = t
try {
    cl()
    assert false
} catch (MissingPropertyException ex) {
    // "age" is not defined on the delegate
}
```


---

# closure in GString

```groovy
def x = 1
def gs = "x = ${x}"
assert gs == 'x = 1'

x = 2
assert gs == 'x = 2'
// -->
def x = 1
def gs = "x = ${-> x}"
assert gs == 'x = 1'

x = 2
assert gs == 'x = 2'
```

```groovy
class Person {
    String name
    String toString() { name }
}
def sam = new Person(name:'Sam')
def lucy = new Person(name:'Lucy')
def p = sam
def gs = "Name: ${p}"
assert gs == 'Name: Sam'
p = lucy
assert gs == 'Name: Sam'
sam.name = 'Lucy'
assert gs == 'Name: Lucy'
// -->
class Person {
    String name
    String toString() { name }
}
def sam = new Person(name:'Sam')
def lucy = new Person(name:'Lucy')
def p = sam
// Create a GString with lazy evaluation of "p"
def gs = "Name: ${-> p}"
assert gs == 'Name: Sam'
p = lucy
assert gs == 'Name: Lucy'
```


---

# closure coercion


---

# functional programming

## currying

```groovy
// left currying
def nCopies = { int n, String str -> str*n }
def twice = nCopies.curry(2)
assert twice('bla') == 'blabla'
assert twice('bla') == nCopies(2, 'bla')


// right currying
def nCopies = { int n, String str -> str*n }
def blah = nCopies.rcurry('bla')
assert blah(2) == 'blabla'
assert blah(2) == nCopies(2, 'bla')


// index based currying
def volume = { double l, double w, double h -> l*w*h }
def fixedWidthVolume = volume.ncurry(1, 2d)
assert volume(3d, 2d, 4d) == fixedWidthVolume(3d, 4d)
def fixedWidthAndHeight = volume.ncurry(1, 2d, 4d)
assert volume(3d, 2d, 4d) == fixedWidthAndHeight(3d)
```


## memoization

```groovy
def fib
fib = { long n -> n<2?n:fib(n-1)+fib(n-2) }
assert fib(15) == 610 // slow!
// -->
fib = { long n -> n<2?n:fib(n-1)+fib(n-2) }.memoize()
assert fib(25) == 75025 // fast!
```


## composition

```groovy
def plus2  = { it + 2 }
def times3 = { it * 3 }

def times3plus2 = plus2 << times3
assert times3plus2(3) == 11
assert times3plus2(4) == plus2(times3(4))

def plus2times3 = times3 << plus2
assert plus2times3(3) == 15
assert plus2times3(5) == times3(plus2(5))

// reverse composition
assert times3plus2(3) == (times3 >> plus2)(3)
```


## trampoline

```groovy
def factorial
factorial = { int n, def accu = 1G ->
    if (n < 2) return accu
    factorial.trampoline(n - 1, n * accu)
}
factorial = factorial.trampoline()

assert factorial(1)    == 1
assert factorial(3)    == 1 * 2 * 3
assert factorial(1000) // == 402387260.. plus another 2560 digits
```


## method pointer

.&
