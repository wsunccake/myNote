# Jenkins


## Package

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


### Other

[Node and Label parameter plugin](https://wiki.jenkins-ci.org/display/JENKINS/NodeLabel+Parameter+Plugin)

[Perforce Plugin](https://wiki.jenkins-ci.org/display/JENKINS/Perforce+Plugin)

[Robot Framework plugin](https://wiki.jenkins-ci.org/display/JENKINS/Robot+Framework+Plugin)