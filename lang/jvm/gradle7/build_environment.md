# build environment

## gradle property

```groovy
// gradle.properties
gradleProperty = value in gradle.properties
```

```groovy
// build.gradle
println gradleProperty
println project.gradleProperty
println project['gradleProperty']
println providers.gradleProperty('gradleProperty').get()
```

---

## system property

```groovy
// gradle.properties
systemProp.system = system property
```

```groovy
// build.gradle
println System.getProperty('system')                // java api
println providers.systemProperty('system').get()    // gradle api
```

```bash
linux:~/demo $ gradle
linux:~/demo $ gradle -D system=myOS
```

---

## project propery

```groovy
// build.gradle
println project.property('projectProp')
println property('projectProp')
println findProperty('projectProp')
println projectProp
```

```bash
linux:~/demo $ gradle
linux:~/demo $ gradle -D projectProp=abc123
```

---

## environment variable

```groovy
// build.gradle
println System.getenv('HOME')                           // java api
println providers.environmentVariable('HOME').get()     // gradle api
```

---

## variable

```groovy
def name = "gradle"
println "hello ${name}"
```
