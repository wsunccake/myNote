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

## script

```groovy
def showInfo(p) { echo "Hi ${p.name}, you are ${p.age}" }
def person = ['name': 'jenkins', 'age': 5]

node {
    stage('Hello') {
        script { showInfo(person) }
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

## input


---

## opt


---

## param

```groovy
node {
    properties([
        parameters([string(defaultValue: '1.0.0.0', name: 'version')])
    ])    
    stage('Build') { echo "Current Version: ${params.version}" }
}
```


---

## env

```groovy
node {
    withEnv(['DB_ENGINE=sqlite']) {
        stage('Hello') {
            sh 'env'
            echo "${env.DB_ENGINE}"
            sh "echo $DB_ENGINE"
        }        
    }
}
```


---

## timeout, retry, waitUntil

```groovy
node {
    stage('timeout') {
        timeout(time: 3, unit: 'SECONDS') {
            sh 'm=`date +%s`; n=`expr $m % 10`; echo $n && sleep $n'
        }
    }

    stage('retry') {
        retry(5) {
            sh 'm=`date +%s`; n=`expr $m % 10`; echo $n; test $n -gt 5 && true || false'
        }
    }

    stage('wait until') {
        waitUntil {
            script {
                def r = sh script: 'm=`date +%s`; n=`expr $m % 10`; echo $n; test $n -gt 5 && true || false', returnStatus: true
                return (r == 0);
            }
        }
    }
}
```

---

## parallel

```
node {
    stage('Hello') {
        echo 'Hello Jenkins2'
    }

    parallel(
        "parallel 1": {
            echo "parallel 1"
        },
        "parallel 2": {
            echo "parallel 2"
        }
    )

    stage('Parallel Hello') {
        parallel(
            "parallel hello 1": {
                echo "parallel hello 1"
            },
            "parallel hello 2": {
                echo "parallel hello 2"
            }
        )
    }

    parallel(
        "parallel stage 1": {
            stage('paralle stage 1') {
                echo 'paralle stage 1'
            }
        },
        "parallel stage 2": {
            stage('parallel stage 2') {
                echo 'parallel stage 2'
            }
        }
    )
}
```

---

## when


---

## post


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
|           +- Bar.groovy
```

`function`

```groovy
// Zot.groovy
def showMessage(msg) {
  echo "${msg}"
}

return this
```

`class`

```groovy
// Bar.groovy
package org.foo

class Bar {
    def steps

    Bar(steps) {
        this.steps = steps
    }

    def show(tasks) {
        steps.echo "bar: ${tasks}"
    }
}
```

`dynamic`

```groovy
node {
    stage('src-function') {
        library (
            identifier: 'dynamic-libary@master', retriever: modernSCM(
                [$class: 'GitSCMSource',
                remote: 'https://git/jenkins-example.git'])
        ).org.foo.Zot.new().showMessage 'show zot'
    }

    stage('src-class') {
        def bar = library (
            identifier: 'dynamic-libary@master', retriever: modernSCM(
                [$class: 'GitSCMSource',
                remote: 'https://git/jenkins-example.git'])
        ).org.foo.Bar.new()
        bar.show('bar')
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


---

## Example

```groovy
node {
    properties([
        parameters([string(defaultValue: '1.2.3.4', name: 'version')])
    ])
    
    currentBuild.displayName = "${params.version} - #${currentBuild.number}"

    stage('S1') {
        echo "Current Version: ${params.version}"
        sh '''#!/bin/bash
echo "${version}"
'''
    }
    
    stage('S2') {
        build job: 'any_job'
    }

    stage('S3') {
        build job: 'always_false', propagate: false
        // build job: 'always_false'
    }
    
    try {
        stage('S4') {
            build job: 'always_false'
        }
    } catch (Exception e) {
        echo "Stage ${currentBuild.result}, but we continue"  
    }

    stage('S5') {
        build job: 'any_job', parameters: [string(name: 'version', value: "${params.version}")]
    }
}
```
