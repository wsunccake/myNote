# Kotlin

## Install

```bash
centos:~ # curl -s https://get.sdkman.io | bash
centos:~ # sdk install kotlin
```

## Hello

### File

```bash
centos:~ # vi hello.kt
fun main(args: Array<String>) {
    println("Hello Kotlin!")
}

centos:~ # kotlinc hello.kt -include-runtime -d hello.jar
centos:~ #  java -jar hello.jar
```

### Inactive

```bash
centos:~ # kotlinc-jvm
>>> println("Hello Kotlin")
```

### Script

```bash
centos:~ # vi hello.kts
println("Hello Kotlin")

centos:~ # kotlinc -script hello.kts
```
