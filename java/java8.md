# Lambda


## Lambda Pros

```
Linux:~ $ mkdir LambdaEx
Linux:~ $ cd LambdaEx
Linux:~/LambdaEx:~ $ gradle init --type java-library
Linux:~/LambdaEx:~ $ tree 
.
├── build.gradle
├── gradle
│   └── wrapper
│       ├── gradle-wrapper.jar
│       └── gradle-wrapper.properties
├── gradlew
├── gradlew.bat
├── settings.gradle
└── src
    ├── main
    │   └── java
    │       └── Library.java
    └── test
        └── java
            └── LibraryTest.java

Linux:~/LambdaEx:~ $ vi build.gradle
group 'com.mycls'
version '1.0-SNAPSHOT'

apply plugin: 'java'

sourceCompatibility = 1.5

repositories {
    mavenCentral()
}

dependencies {
    testCompile group: 'junit', name: 'junit', version: '4.11'
}

Linux:~/LambdaEx:~ $ vi build.gradle
rootProject.name = 'LambdaEx'

Linux:~/LambdaEx:~ $ mkdir -p src/main/java/com/mycls
Linux:~/LambdaEx:~ $ vi src/main/java/com/mycls/Apple.java
package com.myclass;

import java.util.ArrayList;
import java.util.List;
import java.util.jar.Pack200;

public class Apple {
    private int weight = 0;
    private String color = "";

    public Apple(int weight, String color){
        this.weight = weight;
        this.color = color;
    }

    public Integer getWeight() {
        return weight;
    }

    public void setWeight(Integer weight) {
        this.weight = weight;
    }

    public String getColor() {
        return color;
    }

    public void setColor(String color) {
        this.color = color;
    }

    public String toString() {
        return "Apple{" +
               "color='" + color + '\'' +
               ", weight=" + weight +
               '}';
    }

    // method 1.
    public static List<Apple> filterGreenApple(List<Apple> appleList) {
        List<Apple> results = new ArrayList<>();
        for (Apple apple: appleList) {
            if ("green".equals(apple.getColor())) {
                results.add(apple);
            }
        }
        return results;
    }

    public static List<Apple> filterAppleByColor(List<Apple> appleList, String color) {
        List<Apple> results = new ArrayList<>();
        for (Apple apple: appleList) {
            if (color.equals(apple.getColor())) {
                results.add(apple);
            }
        }
        return results;
    }

    public static List<Apple> filterAppleByWeight(List<Apple> appleList, int weight) {
        List<Apple> results = new ArrayList<>();
        for (Apple apple: appleList) {
            if (weight <= apple.getWeight()) {
                results.add(apple);
            }
        }
        return results;
    }

    // method 2.
    public static List<Apple> filterApple(List<Apple> appleList, ApplePredicate predicate) {
        List<Apple> results = new ArrayList<>();
        for (Apple apple: appleList) {
            if (predicate.test(apple)) {
                results.add(apple);
            }
        }
        return results;
    }

    public boolean isRed() {
        return getColor().equals("red");
    }
}

Linux:~/LambdaEx:~ $ vi src/main/java/com/mycls/ApplePredicate.java
package com.myclass;

// functional interface
public interface ApplePredicate {
    public boolean test(Apple apple);
}

Linux:~/LambdaEx:~ $ mkdir -p src/test/java/com/mycls
Linux:~/LambdaEx:~ $ vi src/test/java/com/mycls/AppleTest.java
package com.myclass;

import org.junit.Test;

import java.util.Arrays;
import java.util.List;
import java.util.function.Supplier;

public class AppleTest {
    List<Apple> apples = Arrays.asList(new Apple(50, "green"),
                                       new Apple(150, "red"),
                                       new Apple(100, "green")
                                      );

    @Test
    public void constructorTest() {
        Apple apple = new Apple(10, "red");
        System.out.print(apple);
    }

    @Test
    public void filterGreenAppleTest() {
        List<Apple> results = Apple.filterGreenApple(apples);
        System.out.print(results);
    }

    @Test
    public void filterAppleByColorTest() {
        List<Apple> results1 = Apple.filterAppleByColor(apples, "green");
        List<Apple> results2 = Apple.filterAppleByColor(apples, "red");

        System.out.print(results1);
        System.out.print(results2);
    }

    @Test
    public void filterAppleByWeightTest() {
        List<Apple> results = Apple.filterAppleByWeight(apples, 150);
        System.out.print(results);
    }

    // implement interface
    @Test
    public void filterAppleByImplementInterface() {
        List<Apple> results = Apple.filterApple(apples, new ApplePredicateByColor());
        System.out.print(results);
    }

    // anonymous class
    @Test
    public void filterAppleByAnonymousClass() {
        List<Apple> results = Apple.filterApple(apples, new ApplePredicate() {
            public boolean test(Apple apple){
                return apple.getColor().equals("red");
            }
        });
        System.out.print(results);
    }

    // lambda, -> is functional descriptor
    @Test
    public void filterAppleByLamdba() {
        List<Apple> results = Apple.filterApple(apples, (Apple apple) -> apple.getColor().equals("red"));
        System.out.print(results);
    }

    // method, :: is call method
    @Test
    public void filterAppleBy() {
        List<Apple> results = Apple.filterApple(apples, Apple::isRed);
        System.out.print(results);
    }
}

Linux:~/bean3 $ gradle test
```

## Lambda Express

```
// single line lamdba
// implicit
(int x, int y) -> x + y;

// explicit
(int x, int y) -> {
    return x + y;
}

// multiple line lambda
(int x, int y) -> {
    System.println("x: " + x + ", y: " + y);
    return x + y;
}
```


## Functional Interface

只有定義一個 abstract method in interface

```
public class Java8Tester {

    final static String salutation = "Hello! ";

    public static void main(String args[]){
        // 將 Lambda 帶入 Functional Interface
        GreetingService greetService1 = message -> System.out.println(salutation + message);
        greetService1.sayMessage("Mahesh");
    }

    // 定義 Functional Interface
    interface GreetingService {
        void sayMessage(String message);
    }
}

```


## Method Reference


```
// static method
(args) -> ClassName.staticMethod(args)
=>
ClassName::staticMethod


// expr method
(args) -> expr.instanceMethod(args)
=>
expr::staticMethod


// instance method
(arg0, rest) -> arg0.instanceMethod(rest)
=>
ClassName(arg0.getClass())::instanceMethod
```


```
import java.util.ArrayList;
import java.util.List;

public class Java8Tester {
    public static void main(String[] args) {
        List names = new ArrayList();

        names.add("Mahesh");
        names.add("Suresh");
        names.add("Ramesh");
        names.add("Naresh");
        names.add("Kalpesh");

        // explicit lambda
        names.forEach((name) -> {System.out.println(name);} );
        // implicit lambda
        names.forEach(name -> System.out.println(name));
        // method reference
        names.forEach(System.out::println);
    }
}
```


## Default Method

```
public class Java8Tester {
    public static void main(String args[]) {
        Vehicle vehicle = new Car();
    vehicle.print();
    }
}

interface Vehicle {
    default void print() {
        System.out.println("I am a vehicle!");
    }

    static void blowHorn() {
        System.out.println("Blowing horn!!!");
    }
}

interface FourWheeler {
    default void print() {
        System.out.println("I am a four wheeler!");
    }
}

class Car implements Vehicle, FourWheeler {
    public void print(){
        Vehicle.super.print();
        FourWheeler.super.print();
        Vehicle.blowHorn();
        System.out.println("I am a car!");
    }
}
```


## Stream

```
iimport java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

public class Java8Tester {
    public static void main(String[] args) {
        List<String> names = new ArrayList();

        names.add("Mahesh");
        names.add("");
        names.add("Naresh");
        names.add("");
        names.add("Kalpesh");

        System.out.println(FindNames1(names));
        System.out.println(FindNames2(names));

    }

    static public String FindNames1(List<String> names) {
        StringBuffer result = new StringBuffer();
        for (int i = 0; i < names.size(); i++) {
            if (names.get(i).length() > 1) {
                result.append(capitalize(names.get(i))).append(",");
            }
        }
        return result.subSequence(0, result.length() - 1).toString();
    }

    static public String FindNames2(List<String> names) {
        if (names == null) return "";
        return names.stream()
                .filter(name -> name.length() > 1)
                .map(name -> capitalize(name))
                .collect(Collectors.joining(","));
    }

    static public String capitalize(String e) {
        return e.substring(0, 1).toUpperCase() + e.substring(1, e.length());
    }
}

```