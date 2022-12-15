# application - groovy

## init

```bash
linux:~ $ mkdir demo
linux:~ $ cd demo

# init
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
```

---

## folder

```bash
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
```

---

## task

```bash
# run
linux:~/demo $ gradle run

# test
linux:~/demo $ gradle test

# build
linux:~/demo $ gradle build
linux:~/demo $ ls app/build

# jar
linux:~/demo $ gradle jar
linux:~/demo $ ls app/build/libs

# zip
linux:~/demo $ gradle distZip
linux:~/demo $ ls app/build/distributions

# clean
linux:~/demo $ gradle clean
```
