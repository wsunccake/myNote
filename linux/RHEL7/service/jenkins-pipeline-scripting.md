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

## trigger condition

`cron`

```groovy
node {
    properties([pipelineTriggers([cron('H/2 * * * *')])])
    
    stage('Hello') {
        echo 'Hello World'
    }
}
```

