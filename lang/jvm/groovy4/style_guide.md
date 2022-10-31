# no semicolon


---

# return keyword optional

```groovy
String toString() { return "a server" }
// -->
String toString() { "a server" }
```

```groovy
def foo(n) {
    if(n == 1) {
        "Roshan"
    } else {
        "Dawrani"
    }
}
assert foo(1) == "Roshan"
assert foo(2) == "Dawrani"
```


---

# def and type

```groovy
// variable
def String name = "Guillaume"
// -->
def name = "Guillaume"


// argument
void doSomething(def param1, def param2) { }
// -->
void doSomething(param1, param2) { }


// class
class MyClass {
    def MyClass() {}
}
// -->
class MyClass {
    MyClass() {}
}
```


---

# public by default

```groovy
public class Server {
    public String toString() { return "a server" }
}
// -->
class Server {
    String toString() { return "a server" }
}
```


---

# omitting parentheses

```groovy
println("Hello")
// -->
println "Hello"

method(a, b)
// -->
method a, b

list.each( { println it } )
// -->
list.each(){ println it }
// -->
list.each  { println it }

def foo(n) { n }
println foo 1       // won't work

def bar() { 1 }
def m = bar         // won't work
```


---

# class as first-class citizen

```groovy
connection.doPost(BASE_URI + "/modify.hqu", params, ResourcesResponse.class)
// -->
connection.doPost(BASE_URI + "/modify.hqu", params, ResourcesResponse)
```


---

# getter and setter

```groovy
resourceGroup.getResourcePrototype().getName() == SERVER_TYPE_NAME
// -->
resourceGroup.resourcePrototype.name == SERVER_TYPE_NAME

resourcePrototype.setName("something")
// -->
resourcePrototype.name = "something"

class Person {
    private String name
    String getName() { return name }
    void setName(String name) { this.name = name }
}
// -->
class Person {
    String name
}
```


---

# initializing bean with named parameter and the default constructor

```groovy
class Server {
    String name
    Cluster cluster
}

def server = new Server()
server.name = "Obelix"
server.cluster = aCluster
// -->
def server = new Server(name: "Obelix", cluster: aCluster)
```


---

# using with() and tap() for repeated operations on the same bean

```groovy
server.name = application.name
server.status = status
server.sessionCount = 3
server.start()
server.stop()
// -->
server.with {
    name = application.name
    status = status
    sessionCount = 3
    start()
    stop()
}

def person = new Person().with {
    name = "Ada Lovelace"
    it // Note the explicit mention of it as the return value
}
// -->
def person = new Person().tap {
    name = "Ada Lovelace"
}
```


---

# equals and ==

Java’s == is actually Groovy’s is()

Groovy’s == is a clever equals()

prefer Groovy’s ==, as it also takes care of avoiding NullPointerException

```groovy
status != null && status.equals(ControlConstants.STATUS_COMPLETED)
// -->
status == ControlConstants.STATUS_COMPLETED
```


---

# GString (interpolation, multiline)

```groovy
throw new Exception("Unable to convert resource: " + resource)
// -->
throw new Exception("Unable to convert resource: ${resource}")
// -->
throw new Exception("Unable to convert resource: $resource")
```

```groovy
int i = 3

def s1 = "i's value is: ${i}"
def s2 = "i's value is: ${-> i}"

i++

assert s1 == "i's value is: 3"      // eagerly evaluated, takes the value on creation
assert s2 == "i's value is: 4"      // lazily evaluated, takes the new value into account
```

```groovy
throw new PluginException("Failed to execute command list-applications:" +
    " The group with name " +
    parameterMap.groupname[0] +
    " is not compatible group of type " +
    SERVER_TYPE_NAME)
// -->
throw new PluginException("Failed to execute command list-applications: \
The group with name ${parameterMap.groupname[0]} \
is not compatible group of type ${SERVER_TYPE_NAME}")
// -->
throw new PluginException("""Failed to execute command list-applications:
    The group with name ${parameterMap.groupname[0]}
    is not compatible group of type ${SERVER_TYPE_NAME)}""")
```


---

# native syntax for data structure

```groovy
def list = [1, 4, 6, 9]
def map = [CA: 'California', MI: 'Michigan']

// ranges can be inclusive and exclusive
def range = 10..20              // inclusive
assert range.size() == 11
assert (10..<20).size() == 10   // exclusive

def pattern = ~/fo*/

// equivalent to add()
list << 5

// call contains()
assert 4 in list
assert 5 in list
assert 15 in range

// subscript notation
assert list[1] == 4

// add a new key value pair
map << [WA: 'Washington']
// subscript notation
assert map['CA'] == 'California'
// property notation
assert map.WA == 'Washington'

// matches() strings against patterns
assert 'foo' ==~ pattern
```


---

# groovy development kit

each{}, find{}, findAll{}, every{}, collect{}, inject{}


---

# power of switch

```groovy
def x = 1.23
def result = ""
switch (x) {
    case "foo": result = "found foo"
    // lets fall through
    case "bar": result += "bar"
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
    case { it > 3 }:
        result = "number > 3"
        break
    default: result = "default"
}
assert result == "number"
```


---

# import aliasing

```groovy
import java.util.List as UtilList
import java.awt.List as AwtList
import javax.swing.WindowConstants as WC

UtilList list1 = [WC.EXIT_ON_CLOSE]
assert list1.size() instanceof Integer
def list2 = new AwtList()
assert list2.size() instanceof java.awt.Dimension


import static java.lang.Math.abs as mabs
assert mabs(-4) == 4
```


---

# groovy truth

null, void, equal to zero, or empty evaluates to false

if not, evaluates to true

```groovy
if (name != null && name.length > 0) {}
// -->
if (name) {}
```


---

# safe graph navigation

```groovy
if (order != null) {
    if (order.getCustomer() != null) {
        if (order.getCustomer().getAddress() != null) {
            System.out.println(order.getCustomer().getAddress());
        }
    }
}
// -->
println order?.customer?.address
```


---

# assert

```groovy
def check(String name) {
    // name non-null and non-empty according to groovy truth
    assert name
    // safe navigation + groovy truth to check
    assert name?.size() > 3
}
```


---

# elvis operator for default values

```groovy
def result = name != null ? name : "Unknown"
// -->
def result = name ?: "Unknown"
```


---

# catch any exception

```groovy
try {
    // ...
} catch (Exception t) {
    // something bad happens
}
// -->
try {
    // ...
} catch (any) {
    // something bad happens
}
```


---

# optional typing advice

def