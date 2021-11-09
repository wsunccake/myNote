# jenkins

## install

```bash
# pull image
[linux:~ ] # docker pull jenkins/jenkins:lts

# run container
[linux:~ ] # export JENKINS_HOME=<path>
[linux:~ ] # mkdir -p JENKINS_HOME
[linux:~ ] # docker run -d \
  -v $JENKINS_HOME:/var/jenkins_home \
  -v 8080:8080 \
  -p 50000:50000 \
  [-u <uid>[:<gid>]] \
  --name jenkins \
  [--restart always] \
  jenkins/jenkins:lts
# -d = -detach, -v = --volume, -p = --publish, -u = --user

# install plugin
[linux:~ ] # docker exec -it jenkins sh -c "echo greenballs:latest | /usr/local/bin/install-plugins.sh"

[linux:~ ] # cat plugins.txt
greenballs:latest
[linux:~ ] # docker cp plugins.txt jenkins:/tmp/.
[linux:~ ] # docker exec -it jenkins sh -c "/usr/local/bin/install-plugins.sh < /tmp/plugis.txt"
```
