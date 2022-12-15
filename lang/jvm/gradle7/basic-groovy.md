# basic - groovy

## init

```bash
linux:~ $ mkdir demo
linux:~ $ cd demo
linux:~/demo $ gradle init --type basic --project-name demo
linux:~/demo $ mkdir -p src/main/groovy
```

---

## hello

```groovy
// src/main/groovy/hi.groovy
println("Hi Groovy")
```

```groovy
// settings.gradle
rootProject.name = 'demo'
```

```groovy
// build.gradle
```

```groovy
plugins {
    id 'groovy'
    id 'application'
}

repositories {
    mavenCentral()
}

dependencies {
    implementation group: 'org.apache.groovy', name: 'groovy', version: '4.0.6'
}

application {
    // src/main/groovy/hi.groovy
    mainClass = 'hi'
}

task runScript (dependsOn: 'classes', type: JavaExec) {
    main = 'hi'
    classpath = sourceSets.main.runtimeClasspath
}
```

---

## folder

```bash
linux:~/demo $ tree
.
├── bin
│   └── main
│       └── hi.groovy
├── build.gradle
├── gggg
│   ├── bin
│   │   ├── gggg
│   │   └── gggg.bat
│   └── lib
│       ├── gggg.jar
│       └── groovy-4.0.6.jar
├── gradle
│   └── wrapper
│       ├── gradle-wrapper.jar
│       └── gradle-wrapper.properties
├── gradlew
├── gradlew.bat
├── README.md
├── settings.gradle
└── src
    └── main
        └── groovy
            └── hi.groovy

10 directories, 13 files
```

---

## task

```bash
# build
linux:~/demo $ gradle build

# run
linux:~/demo $ gradle run

# run define task
linux:~/demo $ gradle runScript

# dist
linux:~/demo $ gradle distZip
linux:~/demo $ gradle distTar
linux:~/demo $ ls build/distributions/

# execute
linux:~/demo $ tar build/distributions/demo.tar -C /tmp
linux:~/demo $ /tmp/demo/bin/demo
```
