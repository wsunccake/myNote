## Java Folder Struture

```
<proj>
├── build.gradle
└── src
    └── ratpack
        ├── Ratpack.groovy
        └── static
            ├── css
            │   └── app.css
            ├── index.html
            └── js
                └── app.js
```

## Static Web For Java

```bash
linux:~ # mkdir project
linux:~ # cd project
linux:~/project # gradle init
linux:~/project # mkdir -p src/main/java/my/app
linux:~/project # vi src/main/java/my/app/Main.java
package my.app;

import ratpack.server.BaseDir;
import ratpack.server.RatpackServer;

public class Main {

  public static void main(String[] args) throws Exception {
    RatpackServer.start(spec -> spec
            .serverConfig(c -> c.baseDir(BaseDir.find()).build())
            .handlers(chain -> chain
                    .files(files -> files
                            .dir("static").indexFiles("index.html")
                    )
            )
    );
  }
}

linux:~/project # mkdir -p src/main/resources
linux:~/project # touch src/main/resources/.ratpack

linux:~/project # mkdir -p src/main/resources/static
linux:~/project # vi src/main/resources/static/index.html
<!doctype html>
<html>
<head>
  <title>Welcome to Ratpack!</title>
  <link rel="stylesheet" href="/css/app.css">
</head>
<body>
  <div id="welcome">
    Hello Ratpack!
  </div>

  <script src="/js/app.js"></script>
</body>
</html>

linux:~/project # mkdir -p src/main/resources/static/js
linux:~/project # vi src/main/resources/static/js/app.js
(function() {
  console.log("Welcome to Ratpack!");
})();

linux:~/project # mkdir -p src/main/resources/static/css
linux:~/project # vi src/main/resources/static/css/app.css
#welcome {
  font-size: 28px;
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

apply plugin: 'io.ratpack.ratpack-java'

repositories {
  jcenter()
}

mainClassName = "my.app.Main"

linux:~/project # gradle run

linux:~ # curl http://localhost:5050
```

## Groovy Folder Struture

```
<proj>
├── build.gradle
└── src
    └── main
        ├── java
        │   └── app
        │       └── Main.java
        └── resources
            ├── .ratpack
            └── static
                ├── css
                │   └── app.css
                ├── index.html
                └── js
                    └── app.js
```


## Static Web For Groovy

```bash
linux:~ # mkdir project
linux:~ # cd project
linux:~/project # gradle init
linux:~/project # mkdir -p src/ratpack
linux:~/project # vi src/ratpack/Ratpack.groovy
import static ratpack.groovy.Groovy.ratpack

ratpack {
  handlers {
    files { // <1>
      dir("static").indexFiles("index.html")
    }
  }
}

linux:~/project # mkdir -p src/ratpack/static
linux:~/project # vi src/ratpack/static/index.html
<!doctype html>
<html>
<head>
  <title>Welcome to Ratpack!</title>
  <link rel="stylesheet" href="/css/app.css">
</head>
<body>
  <div id="welcome">
    Hello Ratpack!
  </div>

  <script src="/js/app.js"></script>
</body>
</html>

linux:~/project # mkdir -p src/ratpack/static/js
linux:~/project # vi src/ratpack/static/js/app.js
(function() {
  console.log("Welcome to Ratpack!");
})();

linux:~/project # mkdir -p src/ratpack/static/css
linux:~/project # vi src/ratpack/static/css/app.css
#welcome {
  font-size: 28px;
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

linux:~ # curl http://localhost:5050
```

## Handler

```bash
linux:~ # mkdir project
linux:~ # cd project
linux:~/project # gradle init
linux:~/project # mkdir -p src/ratpack
linux:~/project # vi src/ratpack/Ratpack.groovy
import static ratpack.groovy.Groovy.ratpack
import my.app.FileHandler

ratpack {
  bindings {
    bind FileHandler
  }
  handlers {
    all(FileHandler)
  }
}

linux:~/project # mkdir -p src/ratpack/html
linux:~/project # vi src/ratpack/html/error.html
<!doctype html>
<html>
<body>
Error
</body>
</html>

linux:~/project # vi src/ratpack/html/foo.html
<!doctype html>
<html>
<body>
Foo
</body>
</html>

linux:~/project # vi src/ratpack/html/bar.html
<!doctype html>
<html>
<body>
Bar
</body>
</html>

linux:~/project # mkdir -p src/main/groovy/my/app
linux:~/project # vi src/main/groovy/my/app/FileHandler.groovy

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

linux:~ # curl http://localhost:5050
linux:~ # curl http://localhost:5050?file=foo
linux:~ # curl http://localhost:5050?file=123
```

## Text Templates

```bash
linux:~ # mkdir project
linux:~ # cd project
linux:~/project # gradle init
linux:~/project # mkdir -p src/ratpack
linux:~/project # vi src/ratpack/Ratpack.groovy
import ratpack.groovy.template.TextTemplateModule

import static ratpack.groovy.Groovy.groovyTemplate
import static ratpack.groovy.Groovy.ratpack

ratpack {
  bindings {
    module(TextTemplateModule)
  }
  handlers {
    get {
      render(groovyTemplate(
                [title: "Hello, Ratpack!", 
                welcomeMessage: "Welcome to Learning Ratpack!", 
                footerMessage: "Ratpack is Great!"], "welcome.html"))
    }
  }
}

linux:~/project # mkdir -p src/ratpack/templates
linux:~/project # vi src/ratpack/templates/welcome.html
<!DOCTYPE html>
<html>
<head>
<title>${model.title}</title>
</head>
<body>
${model.welcomeMessage}
<footer>
${model.footerMessage}
</footer>
</body>
</html>

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

linux:~ # curl http://localhost:5050
```

## Markup Template

```bash
linux:~ # mkdir project
linux:~ # cd project
linux:~/project # gradle init
linux:~/project # mkdir -p src/ratpack
linux:~/project # vi src/ratpack/Ratpack.groovy
import ratpack.groovy.template.MarkupTemplateModule

import static ratpack.groovy.Groovy.ratpack
import static ratpack.groovy.Groovy.groovyMarkupTemplate

ratpack {
  bindings {
    module(MarkupTemplateModule)
  }
  handlers {
    get {
      render(groovyMarkupTemplate([
               title: "Hello, Ratpack!", 
               welcomeMessage: "Welcome to Learning Ratpack!", 
               footerMessage: "Ratpack is Great!"], "welcome.gtpl"))
    }
  }
}

linux:~/project # mkdir -p src/ratpack/templates
linux:~/project # vi src/ratpack/templates/welcome.gtpl
html {
  head {
    title(title)
  }
  body {
    yield welcomeMessage
    footer {
      yield footerMessage
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

linux:~ # curl http://localhost:5050
```

## Handlebars.js

```bash
linux:~ # mkdir project
linux:~ # cd project
linux:~/project # gradle init
linux:~/project # mkdir -p src/ratpack
linux:~/project # vi src/ratpack/Ratpack.groovy
import ratpack.handlebars.HandlebarsModule

import static ratpack.groovy.Groovy.ratpack
import static ratpack.handlebars.Template.handlebarsTemplate

ratpack {
  bindings {
    module HandlebarsModule
  }
  handlers {
    get {
      render(handlebarsTemplate("welcome", [
        title: "Hello, Ratpack!", 
        welcomeMessage: "Welcome to Learning Ratpack!", 
        footerMessage: "Ratpack is Great!"], "text/html"))
    }
  }
}

linux:~/project # mkdir -p src/ratpack/handlebars
linux:~/project # vi src/ratpack/handlebars/welcome.hbs
<!DOCTYPE html>
<html>
<head>
<title>{{title}}</title>
</head>
<body>
{{welcomeMessage}}
<footer>
{{footerMessage}}
</footer>
</body>
</html>

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

dependencies {
  compile ratpack.dependency("handlebars")
}

linux:~/project # gradle run

linux:~ # curl http://localhost:5050
```

## Thymeleaf

```bash
linux:~ # mkdir project
linux:~ # cd project
linux:~/project # gradle init
linux:~/project # mkdir -p src/ratpack
linux:~/project # vi src/ratpack/Ratpack.groovy
import ratpack.thymeleaf.ThymeleafModule

import static ratpack.groovy.Groovy.ratpack
import static ratpack.thymeleaf.Template.thymeleafTemplate

ratpack {
  bindings {
    module ThymeleafModule
  }
  handlers {
    get {
      render(thymeleafTemplate([
               title: "Hello, Ratpack!", 
               welcomeMessage: "Welcome to Learning Ratpack!", 
               footerMessage: "Ratpack is Great!"], "welcome"))
    }
  }
}

linux:~/project # mkdir -p src/ratpack/thymeleaf
linux:~/project # vi src/ratpack/thymeleaf/welcome.html
<!DOCTYPE html>
<html>
<head>
<title th:text="${title}" />
</head>
<body th:text="${welcomeMessage}">
<footer th:text="${footerMessage}" />
</body>
</html>

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

dependencies {
  compile ratpack.dependency("thymeleaf")
}

linux:~/project # gradle run

linux:~ # curl http://localhost:5050
```