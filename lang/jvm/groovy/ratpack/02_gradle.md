# Gradle

## Groovy

```bash
linux:~ # mkdir project
linux:~ # cd project
linux:~/project # gradle init
linux:~/project # mkdir -p src/ratpack
linux:~/project # vi src/ratpack/Ratpack.groovy
import static ratpack.groovy.Groovy.ratpack

ratpack {
  handlers {
    get {
      render "Hello, Ratpack!"
    }
  }
}

linux:~/project # vi build.gradle
buildscript {
  repositories {
    jcenter()
  }
  dependencies {
    classpath 'io.ratpack:ratpack-gradle:1.3.3'
  }
}

apply plugin: 'io.ratpack.ratpack-groovy'

repositories {
  jcenter()
}

linux:~/project # gradle run
linux:~/project # gradle -t run
linux:~/project # gradle -t run --debug-jvm 

linux:~/project # curl http://localhost:5050
```

## Java

```bash
linux:~ # mkdir project
linux:~ # cd project
linux:~/project # gradle init
linux:~/project # mkdir -p src/main/java/my/app
linux:~ # vi src/main/java/my/app/Main.java
package my.app;

import ratpack.server.RatpackServer;

public class Main {
   public static void main(String... args) throws Exception {
       RatpackServer.start(server -> server 
            .handlers(chain -> chain
                .get(ctx -> ctx.render("Hello Ratpack!"))
                .get(":name", ctx -> ctx.render("Hello " + ctx.getPathTokens().get("name") + "!"))     
            )
       );
   }
}

linux:~ # vi build.gradle
buildscript {
  repositories {
    jcenter()
  }
  dependencies {
    classpath "io.ratpack:ratpack-gradle:1.5.4"
  }
}

apply plugin: "io.ratpack.ratpack-java"
apply plugin: "idea"

repositories {
  jcenter()
}

dependencies {
  runtime "org.slf4j:slf4j-simple:1.7.25"
}

mainClassName = "my.app.Main"

linux:~/project # gradle run

linux:~ # curl http://localhost:5050
linux:~ # curl http://localhost:5050/kitty
```

##

```
<proj>
 |
 +- src
     |
     +- ratpack
     |     |
     |     +- Ratpack.groovy
     |     +- ratpack.properties
     |     +- public // Static assets in here
     |          |
     |          +- images
     |          +-  lib
     |          +- scripts
     |          +- styles
     |
     +- main
     |   |
     |   +- groovy
     |        |
     |        +- // App classes in here!
     |
     +- test
         |
         +- groovy
              |
              +- // Spock tests in here!
```