# gradle 7.x

## install

```bash
linux:~ # curl -OL https://services.gradle.org/distributions/gradle-7.5.1-all.zip
linux:~ # unzip -d /usr/local gradle-7.5.1-all.zip
linux:~ # ln -s /usr/local/gradle-7.5.1/bin/gradle /usr/local/bin/.

linux:~ $ gradle -h
linux:~ $ gradle -v
linux:~ $ gradle <task>
```


---

## groovy script on gradle

```bash
linux:~ $ mkdir demo
linux:~ $ cd demo
linux:~/demo $ gradle init

Select type of project to generate:
  1: basic
  2: application
  3: library
  4: Gradle plugin
Enter selection (default: basic) [1..4] 1

Select build script DSL:
  1: Groovy
  2: Kotlin
Enter selection (default: Groovy) [1..2] 1

Generate build using new APIs and behavior (some features may change in the next minor release)? (default: no) [yes, no]
Project name (default: demo):

> Task :init
Get more help with your project: Learn more about Gradle by exploring our samples at https://docs.gradle.org/7.5.1/samples

BUILD SUCCESSFUL in 10s
2 actionable tasks: 2 executed

linux:~/demo $ tree
.
├── build.gradle
├── gradle
│   └── wrapper
│       ├── gradle-wrapper.jar
│       └── gradle-wrapper.properties
├── gradlew
├── gradlew.bat
└── settings.gradle

2 directories, 6 files

linux:~/demo $ mkdir -p src/main/groovy
linux:~/demo $ echo 'println("Hi Groovy")' > src/main/groovy/hi.groovy
linux:~/demo $ cat << EOF > build.gradle
apply plugin: 'groovy'

repositories {
    mavenCentral()
}

dependencies {
    implementation group: 'org.apache.groovy', name: 'groovy', version: '4.0.5'
}

task runScript (dependsOn: 'classes', type: JavaExec) {
    main = 'hi'
    classpath = sourceSets.main.runtimeClasspath
}
EOF

linux:~/demo $ gradle run
```


---

## groovy application on gradle

```bash
linux:~ $ mkdir demo
linux:~ $ cd demo
linux:~/demo $ gradle init

Select type of project to generate:
  1: basic
  2: application
  3: library
  4: Gradle plugin
Enter selection (default: basic) [1..4] 2

Select implementation language:
  1: C++
  2: Groovy
  3: Java
  4: Kotlin
  5: Scala
  6: Swift
Enter selection (default: Java) [1..6] 2

Split functionality across multiple subprojects?:
  1: no - only one application project
  2: yes - application and library projects
Enter selection (default: no - only one application project) [1..2] 1

Select build script DSL:
  1: Groovy
  2: Kotlin
Enter selection (default: Groovy) [1..2] 1

Generate build using new APIs and behavior (some features may change in the next minor release)? (default: no) [yes, no] no
Project name (default: demo):
Source package (default: demo):

> Task :init
Get more help with your project: https://docs.gradle.org/7.5.1/samples/sample_building_groovy_applications.html

linux:~/demo $ tree
.
├── app
│   ├── build.gradle
│   └── src
│       ├── main
│       │   ├── groovy
│       │   │   └── demo
│       │   │       └── App.groovy
│       │   └── resources
│       └── test
│           ├── groovy
│           │   └── demo
│           │       └── AppTest.groovy
│           └── resources
├── gradle
│   └── wrapper
│       ├── gradle-wrapper.jar
│       └── gradle-wrapper.properties
├── gradlew
├── gradlew.bat
└── settings.gradle

12 directories, 8 files

linux:~/demo $ gradle tasks
linux:~/demo $ gradle help --task init
linux:~/demo $ gradle init [--dsl groovy] [--type groovy-application]

linux:~/demo $ gradle run
linux:~/demo $ gradle test
linux:~/demo $ gradle build
linux:~/demo $ ls app/build

linux:~/demo $ gradle jar
linux:~/demo $ ls app/build/libs
linux:~/demo $ gradle distZip
linux:~/demo $ ls app/build/distributions

linux:~/demo $ gradle clean
```
