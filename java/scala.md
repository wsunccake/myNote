#

sc 用來寫成 script

scala 用來寫成 java class


## .sc

```
linux:~ # cat upper.sc
class Upper {
  def upper(strings: String*): Seq[String] = {
    strings.map((s:String) => s.toUpperCase())
  }
}

val up = new Upper
println(up.upper("Hello", "Scala"))

linux~: # scala upper.sc
```
script 寫法不需要 main 做程式進入點


## .scala

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


val: immutable variable

var: mutable variable

class:

object: singleton object