# Gradle

## Folder Structure

```
<proj>
 └── src
     │
     ├── ratpack
     │   ├─ Ratpack.groovy
     │   ├─ ratpack.properties
     │   └─ public // Static assets in here
     │      ├─ images
     │      ├─ lib
     │      ├─ scripts
     │      └─ styles
     │
     ├── main
     │   ├─ groovy
     │   │  └─ // App classes in here
     │   └─ java
     │      └─ // App classes in here
     │
     └── test
         └─ groovy
            └─ // Spock tests in here
```


---

## Groovy / Ratpack DSL

`project`

```bash
linux:~ # mkdir project
linux:~ # cd project
linux:~/project # gradle init
```

`code`

```bash
linux:~/project # vi src/ratpack/Ratpack.groovy
import static ratpack.groovy.Groovy.ratpack

ratpack {
  handlers {
    get {
      render "Hello Ratpack!"
    }
  }
}
```

`gradle`

```bash
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
```

`run`

```bash
linux:~/project # gradle run
linux:~/project # gradle -t run
linux:~/project # gradle -t run --debug-jvm 
```

`test`

```
linux:~ # curl http://localhost:5050
```


---

## Java

`project`

```bash
linux:~ # mkdir project
linux:~ # cd project
linux:~/project # gradle init
```

`code`

```bash
linux:~/project # vi src/main/java/my/app/Main.java
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
```

`gradle`

```bash
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
```

`test`

```bash
linux:~ # curl http://localhost:5050
linux:~ # curl http://localhost:5050/kitty
```


---

## Groovy

`code`

```bash
linux:~ # mkdir project
linux:~ # cd project
linux:~/project # gradle init
```

`code`

```bash
linux:~/project # vi src/main/groovy/my/app/Main.groovy
package my.app

import ratpack.groovy.Groovy
import ratpack.server.RatpackServer

class MainGroovy {

  public static void main(String[] args) {
    RatpackServer.start { spec -> spec
      .handlers(Groovy.chain {
        get {
          render "Hello, Ratpack!"
        }
      })
    }
  }
}
```

`gradle`

```bash
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

mainClassName = 'my.app.MainGroovy'

repositories {
  jcenter()
}
```

`test`

```bash
linux:~ # curl http://localhost:5050
```
