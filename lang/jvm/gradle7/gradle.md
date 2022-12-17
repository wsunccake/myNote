# gradle 7

## install

```bash
linux:~ # curl -OL https://services.gradle.org/distributions/gradle-7.5.1-all.zip
linux:~ # unzip -d /usr/local gradle-7.5.1-all.zip
linux:~ # ln -s /usr/local/gradle-7.5.1/bin/gradle /usr/local/bin/.
```

---

## test

```bash
linux:~ $ gradle -h
linux:~ $ gradle -v
```

---

## create project

```bash
linux:~ $ mkdir demo
linux:~ $ cd demo
linux:~/demo $ gradle init
```

---

## usage

```bash
# help
linux:~/demo $ gradle tasks
linux:~/demo $ gradle --help
linux:~/demo $ gradle help --task init

# task
linux:~/demo $ gradle init [--dsl groovy] [--type groovy-application]
linux:~/demo $ gradle tasks [--all] [-b <build file>]
linux:~/demo $ gradle run
linux:~/demo $ gradle test
linux:~/demo $ gradle build
linux:~/demo $ gradle jar
linux:~/demo $ gradle distTar
linux:~/demo $ gradle distZip
linux:~/demo $ gradle clean
```

---

[build environment](./build_environment.md)

[build script basic](./build_script_basic.md)

[basic groovy](./basic-groovy.md)

[application groovy](./application-groovy.md)
