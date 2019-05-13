# Pipeline - scripting syntax

## hello

```groovy
node {
    stage('Hello') {
        echo 'Hello Jenkins2'
    }
}
```

---

## triggers

`cron`

```groovy
node {
    properties([pipelineTriggers([cron('H/2 * * * *')])])
    
    stage('Hello') {
        echo 'Hello World'
    }
}
```


---

## library

### vars

```
(root)
+- vars
|   +- log.groovy
|   +- sayHello.groovy
```

`function`

```groovy
// log.groovy
def info(message) {
    echo "INFO: ${message}"
}
```

`class`

```groovy
// sayHello.groovy
def call(String name = 'human') {
  echo "Hello ${name}"
}
```

`global`

```groovy
library identifier: 'dynamic-libary@master', retriever: modernSCM(
  [$class: 'GitSCMSource',
   remote: 'https://git/jenkins-example.git'])

node {
    stage('vars') {
        sayHello 'Jenkins'
        log.info 'info message'
    }
}
```

`dynamic`

```groovy
node {
    library (
		identifier: 'dynamic-libary@master', retriever: modernSCM(
            [$class: 'GitSCMSource',
            remote: 'https://git/jenkins-example.git'])
	)
	
    stage('vars') {
        sayHello 'Jenkins'
        log.info 'info message'
    }
}
```


### src

```
(root)
+- src/org/foo
|           +- Zot.groovy
```

`function`

```groovy
// Zot.groovy
def showMessage(msg) {
  echo "${msg}"
}

return this
```

```groovy
node {
    stage('src') {
        library (
        identifier: 'dynamic-libary@master', retriever: modernSCM(
            [$class: 'GitSCMSource',
            remote: 'https://git/jenkins-example.git'])
        ).org.foo.Zot.new().showMessage 'show zot'
    }
}
```


## resources


```
(root)
+- resources
|       +- foo.json
```

`foo.json`

```
{
    "version": "0.1"
}
```

`resources`

```groovy
library identifier: 'dynamic-libary@master', retriever: modernSCM(
  [$class: 'GitSCMSource',
   remote: 'https://git/jenkins-example.git'])

def fooJson = libraryResource 'foo.json'

node {
    stage('resources') {
        echo "${fooJson}"
    }
}
```


### vars & src

```groovy
node {
    def lib = library (
	    identifier: 'dynamic-libary@master', retriever: modernSCM(
            [$class: 'GitSCMSource',
            remote: 'https://git/jenkins-example.git'])
	)

    stage('vars') {
        sayHello 'Jenkins'
        log.info 'info message'
    }
    stage('src') {
        lib.org.foo.Zot.new().showMessage 'show zot'
    }
}
```
