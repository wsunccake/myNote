# Pipeline - declarative syntax

## hello

```groovy
pipeline {
    agent any
    stages {
        stage('Hello') {
            steps {
                echo('Hello Jenkins2')
//                sh 'echo "Hello Jenkins2"'
            }
        }
    }
}
```

![pipeline section](./pic/pipeline_section.png)


---

## trigger condition

`cron`

```groovy
pipeline {
    agent any
    triggers {
        cron('H(0-30)/20 * * * *')
    }
    stages {
        stage('Hello') {
            steps {
                echo 'Hello Jenkins2'
            }
        }
    }
}
```


`upstream`

```groovy
pipeline {
    agent any
    triggers {
        upstream(upstreamProjects: 'job1,job2',
                 threshold: hudson.model.Result.SUCCESS)
    }
    stages {
        stage('Hello') {
            steps {
                echo 'Hello Jenkins2'
            }
        }
    }
}
```


---

## input

```groovy
pipeline {
    agent any
    stages {
        stage('Hello') {
            input {
                message "Should continue?"
                parameters {
                    string(name: 'version', defaultValue: '1.0.0.0', description: '')
                }
 
            }
            steps {
                echo "Current Version: ${version}"
            }
        }
    }
}
```


---

## param

```groovy
pipeline {
    agent any
    parameters {
        string(name: 'version', defaultValue: '1.0.0.0', description: '')
    }
    stages {
        stage('Hello') {
            steps {
                echo 'Hello Jenkins2'
            }
        }
        stage('Build') {
            steps {
                echo "Current Version: ${params.version}"
            }
        }
    }
}
```
