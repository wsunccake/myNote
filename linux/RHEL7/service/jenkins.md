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

```
rhel:~ # java -jar jenkins-cli.jar -s http://localhost:8080 list-jobs

rhel:~ # cat <job>.xml | java -jar jenkins-cli.jar -s http://localhost:8080 create-job <job>
rhel:~ # cat <view>.xml | java -jar jenkins-cli.jar -s http://localhost:8080 create-view

rhel:~ # java -jar jenkins-cli.jar -s http://localhost:8080 delete-job <job>
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