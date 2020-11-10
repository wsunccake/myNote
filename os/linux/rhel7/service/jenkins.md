# Jenkins


## Package

```
# setup firewall
rhel~: # firewall-cmd --zone=public --add-port=8080/tcp --permanent
rhel~: # firewall-cmd --zone=public --add-service=http --permanent
rhel~: # firewall-cmd --reload

# update repository and install
rhel:~ # wget -O /etc/yum.repos.d/jenkins.repo http://pkg.jenkins-ci.org/redhat-stable/jenkins.repo
rhel:~ # rpm --import https://jenkins-ci.org/redhat/jenkins-ci.org.key
rhel:~ # yum install jenkins

# setup daemon
rhel:~ # /etc/init.d/jenkins start
rhel:~ # chkconfig jenkins on

rhel:~ # /etc/init.d/jenkins stop
rhel:~ # chkconfig jenkins off
```


### Install via Docker

```
rhel:~ # docker pull jenkins

rhel:~ # docker run -d -p 8080:8080 -p 50000:50000 -v /home/jenkins:/var/jenkins_home jenkins
rhel:~ # docker cp ~/Downloads/p4 <container_id>:/usr/bin/p4
```

----


## CLI


### Jenkins 1.x

```bash
rhel:~ # java -jar jenkins-cli.jar -s http://<jenkins>:8080 help
rhel:~ # java -jar jenkins-cli.jar -s http://<jenkins>:8080 help --help

rhel:~ # java -jar jenkins-cli.jar -s http://<jenkins>:8080 list-jobs [--username <username> --password <password>]
rhel:~ # java -jar jenkins-cli.jar -s http://<jenkins>:8080 build <job> [--username <username> --password <password>] [-p <key>=<val>]

rhel:~ # cat <job>.xml | java -jar jenkins-cli.jar -s http://<jenkins>:8080 create-job <job> [--username <username> --password <password>]
rhel:~ # cat <view>.xml | java -jar jenkins-cli.jar -s http://<jenkins>:8080 create-view [--username <username> --password <password>]

rhel:~ # java -jar jenkins-cli.jar -s http://<jenkins>:8080 delete-job <job> [--username <username> --password <password>]
```


### Jenkins 2.x

```bash
rhel:~ # java -jar jenkins-cli.jar -s http://<jenkins>:8080 help

# auth 1
rhel:~ # java -jar jenkins-cli.jar -s http://<jenkins>:8080 [-auth <username>:<password>] list-jobs

# auth 2
rhel:~ # export JENKINS_USER_ID=<username>
rhel:~ # export JENKINS_API_TOKEN=<password>
rhel:~ # java -jar jenkins-cli.jar -s http://<jenkins>:8080 list-jobs
```


### 1.x different with 2.x

```
     JENKINS_HOME=/var/lib/jenkins
     JOB_BASE_NAME=SSR_NGA_Executor
1.x  WORKSPACE=${JENKINS_HOME}/jobs/${JOB_BASE_NAME}/workspace@2
2.x  WORKSPACE=${JENKINS_HOME}/workspace/${JOB_BASE_NAME}@2
```


----


## Pipeline

`syntax`

```groovy
// Scripted Pipeline
node {
    stage('stage1') {
        echo "Hello Jenkins"
    }

    stage('stage2') {
        sleep 3
        echo "Hello Pipeline"
    }
}

// Declarative Pipeline
pipeline {
    agent any
    stages {
        stage('stage1') {
            steps {
                echo "Hello Jenkins"
                echo "${params.PW}"
                echo "${env.PW}"
                sh "hostname"
            }
        }
        stage('stage2') {
            steps {
                echo "Hi Pipeline"
            }
        }
    }
}
```

`example`

```bash
rhel:~/example # cat Jenkinsfile
node {
    stage('stage') {
        echo "Hello Jenkins"
    }
}

rhel:~/example # git add Jenkinsfile
rhel:~/example # git commit -m "Create Jenkinsfile"
rhel:~/example # git push -u origin master
```


---

## CSRF

disable csrf after 2.222

```bash
rhel:~ # mkdir -p $JENKINS_HOME/init.groovy.d
rhel:~ # cat $JENKINS_HOME/init.groovy.d/csrf.groovy 
import hudson.security.csrf.DefaultCrumbIssuer
import jenkins.model.Jenkins

def jenkins = Jenkins.instance;
jenkins.setCrumbIssuer(null); 
jenkins.save();
```

disable cstf before 2.222

[Disable CSRF checking](https://www.jenkins.io/doc/book/managing/security/#disable-csrf-checking)

---


## Plugin


### Common

[Validating String Parameter Plugin](https://wiki.jenkins-ci.org/display/JENKINS/Validating+String+Parameter+Plugin)

[Slack Notification Plugin](https://wiki.jenkins-ci.org/display/JENKINS/Slack+Plugin)

[Environment Injector Plugin](https://wiki.jenkins-ci.org/display/JENKINS/EnvInject+Plugin)

[Rebuilder](https://wiki.jenkins-ci.org/display/JENKINS/Rebuild+Plugin)

[Multijob plugin](https://wiki.jenkins-ci.org/display/JENKINS/Multijob+Plugin)

[Run Condition Plugin](https://wiki.jenkins-ci.org/display/JENKINS/Run+Condition+Plugin)

[build-name-setter](https://wiki.jenkins-ci.org/display/JENKINS/Build+Name+Setter+Plugin)

[Job Configuration History Plugin](https://wiki.jenkins-ci.org/display/JENKINS/JobConfigHistory+Plugin)

[Naginator Plugin](https://wiki.jenkins-ci.org/display/JENKINS/Naginator+Plugin)

[Build Environment Plugin](https://wiki.jenkins-ci.org/display/JENKINS/Build+Environment+Plugin)

### Other

[Node and Label parameter plugin](https://wiki.jenkins-ci.org/display/JENKINS/NodeLabel+Parameter+Plugin)

[Perforce Plugin](https://wiki.jenkins-ci.org/display/JENKINS/Perforce+Plugin)

[Robot Framework plugin](https://wiki.jenkins-ci.org/display/JENKINS/Robot+Framework+Plugin)
