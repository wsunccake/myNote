# arithmetic operator

```groovy
// normal arithmetic operator
assert  1  + 2 == 3
assert  4  - 3 == 1
assert  3  * 5 == 15
assert  3  / 2 == 1.5
assert 10  % 3 == 1
assert  2 ** 3 == 8


// unary operator
assert +3 == 3
assert -4 == 0 - 4
assert -(-1) == 1

def a = 2
def b = a++ * 3
assert a == 3 && b == 6

def c = 3
def d = c-- * 2
assert c == 2 && d == 6

def e = 1
def f = ++e + 3
assert e == 2 && f == 5

def g = 4
def h = --g + 1
assert g == 3 && h == 4


// assignment arithmetic operator
def a = 4
a += 3
assert a == 7

def b = 5
b -= 3
assert b == 2

def c = 5
c *= 3
assert c == 15

def d = 10
d /= 2
assert d == 5

def e = 10
e %= 3
assert e == 1

def f = 3
f **= 2
assert f == 9
```


---

# relational operator

```groovy
assert 1 + 2 == 3
assert 3 != 4

assert -2 < 3
assert 2 <= 2
assert 3 <= 4

assert 5 > 1
assert 5 >= -2
```

```groovy
import groovy.transform.EqualsAndHashCode

@EqualsAndHashCode
class Creature { String type }

def cat = new Creature(type: 'cat')
def copyCat = cat
def lion = new Creature(type: 'cat')

assert cat.equals(lion) // Java logical equality
assert cat == lion      // Groovy shorthand operator

assert cat.is(copyCat)  // Groovy identity
assert cat === copyCat  // operator shorthand
assert cat !== lion     // negated operator shorthand
```


---

# logical operator

```groovy
assert !false
assert true && true
assert true || false


// precedence
assert (!false && false) == false
assert true || true && false


// short-circuiting
boolean checkIfCalled() {
    called = true
}

called = false
true || checkIfCalled()
assert !called

called = false
false || checkIfCalled()
assert called

called = false
false && checkIfCalled()
assert !called

called = false
true && checkIfCalled()
assert called
```


---

# bitwise and bit shift operator

```groovy
// bitwise operator
int a = 0b00101010
assert a == 42
int b = 0b00001000
assert b == 8
assert (a & a) == a
assert (a & b) == b
assert (a | a) == a
assert (a | b) == a

int mask = 0b11111111
assert ((a ^ a) & mask) == 0b00000000
assert ((a ^ b) & mask) == 0b00100010
assert ((~a) & mask)    == 0b11010101


// bit shift operator
assert 12.equals(3 << 2)
assert 24L.equals(3L << 3)
assert 48G.equals(3G << 4)

assert 4095 == -200 >>> 20
assert -1 == -200 >> 20
assert 2G == 5G >> 1
assert -3G == -5G >> 1
```


---

# conditional operator

```groovy
// not operator
assert (!true)    == false
assert (!'foo')   == false
assert (!'')      == true


// ternary operator
if (string!=null && string.length()>0) {
    result = 'Found'
} else {
    result = 'Not found'
}

result = (string!=null && string.length()>0) ? 'Found' : 'Not found'

result = string ? 'Found' : 'Not found'


// elvis operator
displayName = user.name ? user.name : 'Anonymous'
displayName = user.name ?: 'Anonymous'


// elvis assignment operator
import groovy.transform.ToString

@ToString
class Element {
    String name
    int atomicNumber
}

def he = new Element(name: 'Helium')
he.with {
    name = name ?: 'Hydrogen'   // existing Elvis operator
    atomicNumber ?= 2           // new Elvis assignment shorthand
}
assert he.toString() == 'Element(Helium, 2)'
```


---

# object operator

```groovy
// safe navigation operator - ?.
def person = Person.find { it.id == 123 }
def name = person?.name     // person.name
assert name == null


// direct field access operator - .@
class User {
    public final String name
    User(String name) { this.name = name}
    String getName() { "Name: $name" }
}
def user = new User('Bob')
assert user.name == 'Name: Bob'
assert user.@name == 'Bob'


// method pointer operator - .&
def str = 'example of method reference'
def fun = str.&toUpperCase
def upper = fun()
assert upper == str.toUpperCase()

def transform(List elements, Closure action) {
    def result = []
    elements.each {
        result << action(it)
    }
    result
}
String describe(Person p) {
    "$p.name is $p.age"
}
def action = this.&describe
def list = [
    new Person(name: 'Bob',   age: 42),
    new Person(name: 'Julia', age: 35)]
assert transform(list, action) == ['Bob is 42', 'Julia is 35']

// method pointer operator - overload
def doSomething(String str) { str.toUpperCase() }
def doSomething(Integer x) { 2*x }
def reference = this.&doSomething
assert reference('foo') == 'FOO'
assert reference(123)   == 246

def foo  = BigInteger.&new
def fortyTwo = foo('42')
assert fortyTwo == 42G

def instanceMethod = String.&toUpperCase
assert instanceMethod('foo') == 'FOO'


// method reference operator
import groovy.transform.CompileStatic
import static java.util.stream.Collectors.toList

@CompileStatic
void methodRefs() {
    assert 6G == [1G, 2G, 3G].stream().reduce(0G, BigInteger::add)
    assert [4G, 5G, 6G] == [1G, 2G, 3G].stream().map(3G::add).collect(toList())
    assert [1G, 2G, 3G] == [1L, 2L, 3L].stream().map(BigInteger::valueOf).collect(toList())
    assert [1G, 2G, 3G] == [1L, 2L, 3L].stream().map(3G::valueOf).collect(toList())
}
methodRefs()

@CompileStatic
void constructorRefs() {
    assert [1, 2, 3] == ['1', '2', '3'].stream().map(Integer::new).collect(toList())
    def result = [1, 2, 3].stream().toArray(Integer[]::new)
    assert result instanceof Integer[]
    assert result.toString() == '[1, 2, 3]'
}
constructorRefs()
```


---

# regular expression operator

```groovy
// pattern operator - ~
def p = ~/foo/
assert p instanceof Pattern

p = ~'foo'
p = ~"foo"
p = ~$/dollar/slashy $ string/$
p = ~"${pattern}"


// find operator - =~
def text = "some text to match"
def m = text =~ /match/
assert m instanceof Matcher
if (!m) {
    throw new RuntimeException("Oops, text not found!")
}


// match operator - ==~
m = text ==~ /match/
assert m instanceof Boolean
if (m) {
    throw new RuntimeException("Should not reach that point!")
}


// comparing find vs match operator
assert 'two words' ==~ /\S+\s+\S+/
assert 'two words' ==~ /^\S+\s+\S+$/
assert !(' leading space' ==~ /\S+\s+\S+/)

def m1 = 'two words' =~ /^\S+\s+\S+$/
assert m1.size() == 1
def m2 = 'now three words' =~ /^\S+\s+\S+$/
assert m2.size() == 0
def m3 = 'now three words' =~ /\S+\s+\S+/
assert m3.size() == 1
assert m3[0] == 'now three'
def m4 = ' leading space' =~ /\S+\s+\S+/
assert m4.size() == 1
assert m4[0] == 'leading space'
def m5 = 'and with four words' =~ /\S+\s+\S+/
assert m5.size() == 2
assert m5[0] == 'and with'
assert m5[1] == 'four words'
```


---

# other operator

## spread operator

```groovy
// spread operator - *.
class Car {
    String make
    String model
}
def cars = [
       new Car(make: 'Peugeot', model: '508'),
       new Car(make: 'Renault', model: 'Clio')]
def makes = cars*.make
assert makes == ['Peugeot', 'Renault']

cars = [
   new Car(make: 'Peugeot', model: '508'),
   null,
   new Car(make: 'Renault', model: 'Clio')]
assert cars*.make == ['Peugeot', null, 'Renault']
assert null*.make == null

class Component {
    Long id
    String name
}
class CompositeObject implements Iterable<Component> {
    def components = [
        new Component(id: 1, name: 'Foo'),
        new Component(id: 2, name: 'Bar')]

    @Override
    Iterator<Component> iterator() {
        components.iterator()
    }
}
def composite = new CompositeObject()
assert composite*.id == [1,2]
assert composite*.name == ['Foo','Bar']

class Make {
    String name
    List<Model> models
}

@Canonical
class Model {
    String name
}

def cars = [
    new Make(name: 'Peugeot',
             models: [new Model('408'), new Model('508')]),
    new Make(name: 'Renault',
             models: [new Model('Clio'), new Model('Captur')])
]

def makes = cars*.name
assert makes == ['Peugeot', 'Renault']

def models = cars*.models*.name
assert models == [['408', '508'], ['Clio', 'Captur']]
assert models.sum() == ['408', '508', 'Clio', 'Captur']         // flatten one level
assert models.flatten() == ['408', '508', 'Clio', 'Captur']     // flatten all levels (one in this case)

// collectNested
class Car {
    String make
    String model
}
def cars = [
   [
       new Car(make: 'Peugeot', model: '408'),
       new Car(make: 'Peugeot', model: '508')
   ], [
       new Car(make: 'Renault', model: 'Clio'),
       new Car(make: 'Renault', model: 'Captur')
   ]
]
def models = cars.collectNested{ it.model }
assert models == [['408', '508'], ['Clio', 'Captur']]


// spreading method argument
int function(int x, int y, int z) {
    x*y+z
}
def args = [4,5,6]
assert function(*args) == 26

args = [4]
assert function(*args,5,6) == 26


// spread list element
def items = [4,5]
def list = [1,2,3,*items,6]
assert list == [1,2,3,4,5,6]


// spread map element
def m1 = [c:3, d:4]
def map = [a:1, b:2, *:m1]
assert map == [a:1, b:2, c:3, d:4]

def m1 = [c:3, d:4]
def map = [a:1, b:2, *:m1, d: 8]
assert map == [a:1, b:2, c:3, d:8]
```


## range operator

```groovy
// range operator - ..
def range = 0..5
assert (0..5).collect() == [0, 1, 2, 3, 4, 5]
assert (0..<5).collect() == [0, 1, 2, 3, 4]
assert (0<..5).collect() == [1, 2, 3, 4, 5]
assert (0<..<5).collect() == [1, 2, 3, 4]
assert (0..5) instanceof List
assert (0..5).size() == 6

assert ('a'..'d').collect() == ['a','b','c','d']
```


## spaceship operator

```groovy
// spaceship operator - <=>
assert (1 <=> 1) == 0
assert (1 <=> 2) == -1
assert (2 <=> 1) == 1
assert ('a' <=> 'z') == -1
```


## subscript operator

```groovy
// subscript operator - getAt / putAt
def list = [0,1,2,3,4]
assert list[2] == 2
list[2] = 4
assert list[0..2] == [0,1,4]
list[0..2] = [6,6,6]
assert list == [6,6,6,3,4]

class User {
    Long id
    String name
    def getAt(int i) {
        switch (i) {
            case 0: return id
            case 1: return name
        }
        throw new IllegalArgumentException("No such element $i")
    }
    void putAt(int i, def value) {
        switch (i) {
            case 0: id = value; return
            case 1: name = value; return
        }
        throw new IllegalArgumentException("No such element $i")
    }
}
def user = new User(id: 1, name: 'Alex')
assert user[0] == 1
assert user[1] == 'Alex'
user[1] = 'Bob'
assert user.name == 'Bob'
```


## safe index operator

```groovy
// safe index operator - ?[]
String[] array = ['a', 'b']
assert 'b' == array?[1]      // get using normal array index
array?[1] = 'c'              // set using normal array index
assert 'c' == array?[1]

array = null
assert null == array?[1]     // return null for all index values
array?[1] = 'c'              // quietly ignore attempt to set value
assert null == array?[1]

def personInfo = [name: 'Daniel.Sun', location: 'Shanghai']
assert 'Daniel.Sun' == personInfo?['name']      // get using normal map index
personInfo?['name'] = 'sunlan'                  // set using normal map index
assert 'sunlan' == personInfo?['name']

personInfo = null
assert null == personInfo?['name']              // return null for all map values
personInfo?['name'] = 'sunlan'                  // quietly ignore attempt to set value
assert null == personInfo?['name']


// membership operator - in
def list = ['Grace','Rob','Emmy']
assert ('Emmy' in list)


// identity operator - is
def list1 = ['Groovy 1.8','Groovy 2.0','Groovy 2.3']
def list2 = ['Groovy 1.8','Groovy 2.0','Groovy 2.3']
assert list1 == list2
assert !list1.is(list2)


// coercion operator - as
Integer x = 123
String s = (String) x

Integer x = 123
String s = x as String

class Identifiable {
    String name
}
class User {
    Long id
    String name
    def asType(Class target) {
        if (target == Identifiable) {
            return new Identifiable(name: name)
        }
        throw new ClassCastException("User cannot be coerced into $target")
    }
}
def u = new User(name: 'Xavier')
def p = u as Identifiable
assert p instanceof Identifiable
assert !(p instanceof User)


// diamond operator - <>
List<String> strings = new LinkedList<>()


// call operator - call
class MyCallable {
    int call(int x) {
        2*x
    }
}

def mc = new MyCallable()
assert mc.call(2) == 4
assert mc(2) == 4
```


---

## operator precedence


---

## operator overloading

```groovy
class Bucket {
    int size

    Bucket(int size) { this.size = size }

    Bucket plus(Bucket other) {
        return new Bucket(this.size + other.size)
    }
}

def b1 = new Bucket(4)
def b2 = new Bucket(11)
assert (b1 + b2).size == 15

assert (b1 + 11).size == 15
Bucket plus(int capacity) {
    return new Bucket(this.size + capacity)
}
```
