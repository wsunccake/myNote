# container app

## jenkins

```bash
# pull image
[centos:~ ] # podman pull jenkins/jenkins:lts

# run container
[centos:~ ] # export JENKINS_HOME=<path>
[centos:~ ] # podman run --detach --volume $JENKINS_HOME:/var/jenkins_home --publish 8080:8080 --publish 50000:50000 --user root --name jenkins jenkins/jenkins:lts

# install plugin
[centos:~ ] # podman exec -it jenkins sh -c "echo greenballs:latest | /usr/local/bin/install-plugins.sh"

[centos:~ ] # cat plugins.txt
greenballs:latest
[centos:~ ] # podman cp plugins.txt jenkins:/tmp/.
[centos:~ ] # podman exec -it jenkins sh -c "/usr/local/bin/install-plugins.sh < /tmp/plugis.txt"
```


---
