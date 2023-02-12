# build script basic

## hello world

```groovy
// build.gradle
task hi {
    doLast {
        println "hi gradle"
    }
}

tasks.create("hey") {
    doLast {
        println "hey gradle"
    }
}

tasks.register("hello") {
    doLast {
        println "hello gradle"
    }
}

tasks.register('something') {
    doLast {
        String someString = 'mY_nAmE'
        println "Original: $someString"
        println "Upper case: ${someString.toUpperCase()}"

        4.times { print "$it " }

        println name
        println project.name
    }
}
```

```bash
linux:~/demo $ gradle tasks --all
linux:~/demo $ gradle -q hi
linux:~/demo $ gradle -q hey
linux:~/demo $ gradle -q hello
linux:~/demo $ gradle -q something
```

---

## task dependency

### declaration of task that depends on other task

```groovy
// build.gradle
tasks.register('hello') {
    doLast {
        println 'Hello world!'
    }
}

tasks.register('intro') {
    dependsOn tasks.hello
    doLast {
        println "I'm Gradle"
    }
}
```

```groovy
task hello {
    doLast {
        println 'Hello world!'
    }
}

task intro (dependsOn: [hello]) {
    doLast {
        println "I'm Gradle"
    }
}
```

### lazy dependsOn - the other task does not exist

```groovy
// build.gradle
tasks.register('taskX') {
    dependsOn 'taskY'
    doLast {
        println 'taskX'
    }
}

tasks.register('taskY') {
    doLast {
        println 'taskY'
    }
}
```

---

## flexible task registration

```groovy
// build.gradle
4.times { counter ->
    tasks.register("task$counter") {
        doLast {
            println "task $counter"
        }
    }
}
```

---

## manipulating existing task

```groovy
// build.gradle
4.times { counter ->
    tasks.register("task$counter") {
        doLast {
            println "task $counter"
        }
    }
}
tasks.named('task0') { dependsOn('task2', 'task3') }
```

```groovy
// build.gradle
tasks.register('hello') {
    doLast {
        println 'Hello Earth'
    }
}
tasks.named('hello') {
    doFirst {
        println 'Hello Venus'
    }
}
tasks.named('hello') {
    doLast {
        println 'Hello Mars'
    }
}
tasks.named('hello') {
    doLast {
        println 'Hello Jupiter'
    }
}
```

---

## default task

```groovy
// build.gradle
defaultTasks 'clean', 'run'

tasks.register('clean') {
    doLast {
        println 'Default Cleaning!'
    }
}

tasks.register('run') {
    doLast {
        println 'Default Running!'
    }
}

tasks.register('other') {
    doLast {
        println "I'm not a default task!"
    }
}
```

---

## external dependencies for the build script

```groovy
// build.gradle
import org.apache.commons.codec.binary.Base64

buildscript {
    repositories {
        mavenCentral()
    }
    dependencies {
        classpath group: 'commons-codec', name: 'commons-codec', version: '1.2'
    }
}

tasks.register('encode') {
    doLast {
        def byte[] encodedString = new Base64().encode('hello world\n'.getBytes())
        println new String(encodedString)
    }
}
```
