# java

## install

```bash
# install
alma:~ # dnf -y install java-1.8.0-openjdk java-1.8.0-openjdk-devel
alma:~ # dnf -y install java-11-openjdk java-11-openjdk-devel
alma:~ # dnf -y install java-17-openjdk java-17-openjdk-devel

# setting
alma:~ # alternatives --config java
alma:~ # alternatives --config javac
# /var/lib/alternatives/java, /var/lib/alternatives/javac

# checking
alma:~ # java -version
alma:~ # javac -version
```
