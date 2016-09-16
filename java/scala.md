# Scala

sc 用來寫成 script

scala 用來寫成 java class


## Intro


### REPL

Scala 也有類似 Python 的 python/ipython, Ruby 的 irb, Groovy 的  groovysh 的 REPL (Read–Eval–Print Loop) 操作模式

```
linux:~ # scala -help
linux:~ # scala -version
linux:~ # scala
scala> println("Hello Scala!")
```


### .sc

```
linux:~ # cat upper.sc
class Upper {
  def upper(strings: String*): Seq[String] = {
    strings.map((s:String) => s.toUpperCase())
  }
}

val up = new Upper
println(up.upper("Hello", "Scala"))

linux:~ # scala upper.sc
```
script 寫法不需要 main 做程式進入點


### .scala

```
linux:~ # cat Upper.scala
object Upper {
  def upper(strings: String*) : Seq[String] = strings.map(_.toUpperCase())

  def main(args: Array[String]) {
    println(this.upper("Hello", "scala"))
  }
}

linux:~ # scalac Upper.scala
linux:~ # scala Upper
```

java class 用法需要先編譯成 class, 才能執行


### sbt

sbt (simple build tool) 是 scala 的 build tool

```
linux:~ # mkdir scalaProject
linux:~ # cd scalaProject
linux:~ #mkdir -p src/main/scala
linux:~/scalaProject # vi hw.scala
linux:~/scalaProject # object Hi {
    def main(args: Array[String]) = println("Hi!")
}
linux:~/scalaProject # cat build.sbt
name := "hello"
version := "1.0"
scalaVersion := "2.11.2"
linux:~/scalaProject # sbt run
```

----


## Data Type

![Scala](https://www.safaribooksonline.com/library/view/learning-scala/9781449368814/images/lnsc_0201.png.jpg)


### Vaule and Variable


Scala 變數宣告可以分為 val, var 兩種, val 是宣告不變量, var 是宣告變量

```
val <identifer>[: <type>] = <literal> | <data> | <expression>
var <identifer>[: <type>] = <literal> | <data> | <expression>
```

```
val val1 = 1
// val1 = 10         // val1 不可再 assgin
val val2: Int = 2
val val3: String = "abc" * val2
val val4 : Int = {
  val val5 = 4
  val5 + 4
}

println("val3:" + $val3)

var var1 = 1
var var2: Int = 2
var var3: String = "abc" * var2
var1 = 10

println("val3:" + $var3)
```


### Numerical Data

Scala 的數值資料 Byte, Short, Int, Long, Float, Double. 但 Scala 不像 Java 有 primitive data type, Scala 中的 Int 跟 Java int 不一樣.


### String

```
val s1 = "Hello"
val s2 = "Scala"

// string concat
val s3 = s1 + " " + s2

// string interpolation
val s4 = s"$s1 ${s2}"
val height = 1.9d
val name = "James"
val s5 = f"$name%s is $height%2.2f meters tall"

// multi line string
val s6 ="""
a1
a2
"""
val s7 =
  """a1
    |a2
  """.stripMargin
val s8 =
  """a1
    |a2
  """.stripMargin.replaceAll("\n", ",")
```

### Unit

Unit 相當是 Java 中的 void, 多用於 function 或 method

### Tuple


### Seq

![Seq Class](https://www.safaribooksonline.com/library/view/learning-scala/9781449368814/images/lnsc_0701.png.jpg)

### List

List 是 Immutable Collection

```
// empty list
val l1 = List()
l1.isEmpty
l1 == Nil

// list
val l2: List[String] = List("mon", "tue", "wed", "thu", "fri", "sat", "sun")
l2.head
l2.last
l2.size
for (day: String <- l2) println(day)
l2.foreach((day: String) => println(day))

// element prepend and append
var l3 = 1 :: 2 :: Nil
l3 = 0 :: l3
l3 = l3 :+ 4
l3.patch(2, Nil, 1)

// list concat
val l4 = List(1, 2)
val l5 = 3 :: 4 :: Nil
val l6 = l5 ::: l4
l6.reverse
l6.sorted
```


### Set

Set 是 Immutable Collection

```
val s1 = Set()
s1.isEmpty

val s2 = Set(1, 2, 3, 1, 2, 3)
s2.size
```

### Map

Map 是 Immutable Collection

```
val colorMap: Map[String, Int] = Map("red" -> 0xFF0000, "green" -> 0xFF00, "blue" -> 0xFF)
for (m <- colorMap) println(m)
for (k <- colorMap.keys) println(s"$k -> ${colorMap(k)}")
for ((k, v) <- colorMap) println(s"$k -> $v")
colorMap.foreach(m => println (s"${m._1} -> ${m._2}"))
colorMap.foreach {case (k, v) => println(s"$k -> $v")}

```

----


## Condition

### If Else

```
if (<boolean expression>)
  <expression>

if (<boolean expression>)
  <expression>
else
  <expression>
```

```
val os: String = System.getProperty("os.name")
var o: String = null

if (os == "Linux") {
  o = "Linux"
} else {
  o = "Unknown"
}
println(s"OS: $o")

// 另一種簡單方式的 if/else 使用方式
var o: String = if (os == "Linux") "Linux" else "Unknow"
```

```
val input: String = scala.io.StdIn.readLine("input your sex [m/f]: ")
val sex: String = if (input == "m")
  "Male"
else if (input == "f")
  "Female"
else
  "Unknown"

println(s"Sex: $sex")
```


### Pattern Matching

```
<expression> match {
  case <pattern> [| <pattern> | ...] => <expression>
  [case ...]
  [case <pattern> if <boolean expression> => <expression>]
  [case <identifer>[: <type>] => <expression>]
}
```

```
val input: String = scala.io.StdIn.readLine("input your sex [m/f]: ")
val sex: String = input match {
  case "m" =>
    "Male"
  case "f" =>
    "Female"
  case _ =>
    "Unknown"
}

println(s"Sex: $sex")
```

```
val day: String = scala.io.StdIn.readLine("input day")
val d: String = day.toLowerCase() match {
  case "mon" | "tue" | "wed" | "thu" | "fri" =>
    "workday"
  case "sat" | "sun" =>
    "weekend"
}
```


### For

```
for (<identifer>[: <type>] <- <iterator> [if <boolean expression>] [yield]
  <expression>
```

```
// 數值迴圈的使用方式 
// 1 ~ 5, 間格為 2
for (i: Int <- 1 to 5 by 2)
  println(i)

// 1 ~ 4
for (j: Int <- 1 until 5) println(j)

// 將結果做成集合且回傳
val odds = for (i: Int <- 1 to 5 if i % 2 ==0) yield i
println(odds)
```


### While

```
var input: String = scala.io.StdIn.readLine("Input the word, [Quit]")
while (input != "Quit") {
  println(s"Your keyin: $input")
  input = scala.io.StdIn.readLine("Input the word, [Quit]")
}
```

----


## Function


### def

```
def <function identifer> [(<argument>[: <type>= <value> [...]]:<type>)] = <expression>

<function identifer>(<argument>)

<function identifer> {<expression>} 
```

```
// 定義沒有 argument 的 function
def hi1(): Unit = println("Hi")
hi1()     // call function
hi1       // 沒 argument 可省略 ()

// 另一種定義沒有 argument 的 function
def hi2 = println("Hi")
hi 2      // call function
// hi2()  // 因為定義沒用 (), 在使用 () 則會錯誤

// 定義有 argument 的 function
def sayHi1(s: String): String = s"Hi $s"
sayHi1("Scala")

// 定義有 default value argument 的 function
def sayHi2(s: String= "Scala"):String = {
  s"Hi $s"
}
sayHi2()
sayHi2("scala")
sayHi1("Scala")
sayHi2()
sayHi2("scala")
sayHi2 {   // 當只有一個 argurment, 可使用 expression 代替
  val firstName:String = "Martin"
  val lastName: String = "Odersky"
  s"$firstName $lastName"
}

// vararg, 不定 argument 數目
def sum(i: Int*): Int = {
  var total = 0
  for (j: Int <- i) {
    total = total + j
  }
  total
}
sum(1, 2, 3)
```

```
def <function identifer>[<type name>](<argument>: <type name>) = <expression>
```

```
def f1(s: String): String = s
def f1(i: Int): Int = i
f1("Scala")
f1(1)

def f2[A](a: A): A = a
f2[String]("Scala")
f2(1)
```


### First-Class Function

把 function 當成 value 或 variable 使用

```
(<type>, ...) => <type>
val <identifer>: (<type, ...) => <type> = <function identifer>
val <identifer> = <function identifer> _
```

```
def double(x: Int): Int = x * 2
val double1: (Int) => Int = double
double1(1)
val double2 = double _
double2(1)
```


### Higher-order Function

```
def <function identifer>((<type>, ...) => <type>, ...) = <expression>
```

把 function 當成 argument 使用

```
import scala.collection.mutable.ListBuffer

val l1 = List(1, 2, 3)

def doList1(l: List[Int]): List[Int] = {
  val result: ListBuffer[Int] = ListBuffer()
  for (i: Int <- l) {
    result += 2 * i
  }
  result.toList
}
println(doList1(l1))

// define higher-order function
def doList2(l: List[Int], f: Int => Int): List[Int] = {
  val result: ListBuffer[Int] = ListBuffer()
  for (i: Int <- l) {
    result += f(i)
  }
  result.toList
}

def double(i: Int): Int = i * 2
val d1 = double _

// d1 當 argument 傳入 function
println(doList2(l1, d1))
```


### Function Literal

function literal 概念和 anonymous function, lambda expressoion

```
// 延續 Higher-order Function 範例
println(doList2(l1, (i: Int) => i * 3))
println(doList2(l1, i => i * 3))           // 使用更簡潔 function literal
println(doList2(l1, _ * 3))                // 使用 _ 代替 (placeholder syntax)
```


### Partially Apply

partially apply 使將 function 部分 argument 設定 再轉給另一個 function 使用

```
def factorOf(x: Int, y: Int) = y % x == 0
val f = factorOf _
f(3 ,21)

// partially apply
val mulitple3 = factorOf(3, _: Int)
mulitple3(21)
```


### Currying

```
def factorOf(x: Int)(y: Int) = y % x == 0
val f = factorOf _
f(3)(21)

// currying
val mulitple3 = factorOf(3) _
mulitple3(21)
```


### Partially Function

partially function 是將 function 的 argument 並非全部都適用函數內部執行

```
def httpStatus1(returnCode: Int): String = {
  returnCode match {
    case 200 => "Ok"
    case 400 => "Client Error"
    case 500 => "Server Error"
  }
}
httpStatus1(200)
// httpStatus1(404)   // 會有 MatchError

val httpStatus2: Int => String = {
    case 200 => "Ok"
    case 400 => "Client Error"
    case 500 => "Server Error"
}
httpStatus2(200)
// httpStatus2(404)   // 會有 MatchError

val httpStatus3 = PartialFunction[Int, String] {
  case 200 => "Ok"
  case 400 => "Client Error"
  case 500 => "Server Error"
}
httpStatus3(200)
httpStatus3(404)   // 會有 MatchError
```


----


