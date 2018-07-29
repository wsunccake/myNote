# Handler


## Simple

```bash
linux:~ # mkdir project
linux:~ # cd project
linux:~/project # gradle init
linux:~/project # mkdir -p src/ratpack
linux:~/project # vi src/ratpack/Ratpack.groovy
import static ratpack.groovy.Groovy.ratpack
import ratpack.handling.Handler
import ratpack.handling.Context

class DefaultRouteHandler implements Handler {
  private final String defaultMessage

  DefaultRouteHandler(String message) {
    this.defaultMessage = message
  }

  @Override
  void handle(Context context) {
    if (context.pathTokens.containsKey("name")) {
      context.render "Hello, ${context.pathTokens.name}!"
    } else {
      context.render defaultMessage
    }
  }
}

ratpack {
  bindings {
    add(new DefaultRouteHandler("Hello, Ratpack!"))
  }
  handlers {
    get(DefaultRouteHandler)
    get(":name", DefaultRouteHandler)
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
linux:~ # curl http://localhost:5050/kitty
```


---

## Complex

```bash
linux:~ # mkdir project
linux:~ # cd project
linux:~/project # gradle init
linux:~/project # mkdir -p src/ratpack
linux:~/project # vi src/ratpack/Ratpack.groovy
import ratpack.handling.Context
import ratpack.handling.Handler
import ratpack.registry.Registry

import static ratpack.groovy.Groovy.ratpack
import static ratpack.jackson.Jackson.json

class UserAgentVersioningHandler implements Handler {
  private static final String ERROR_MSG = "Unsupported User Agent"

  enum ClientVersion {
    V1("Microservice Client v1.0"),
    V2("Microservice Client v2.0"),
    V3("Microservice Client v3.0")

    String versionString

    ClientVersion(String versionString) {
      this.versionString = versionString
    }

    static ClientVersion fromString(String versionString) {
      for (val in values()) {
        if (val.versionString == versionString) {
          return val

        }
      }
      null
    }
  }

  @Override
  void handle(Context context) {
    def userAgent = context.request.headers.get("User-Agent") // <1>
    def clientVersion = ClientVersion.fromString(userAgent)
    if (!clientVersion) {
      renderError(context)
    } else {
      context.next(Registry.single(ClientVersion, clientVersion)) // <2>
    }
  }

  private static void renderError(Context context) {
    context.response.status(400)
    context.byContent { spec ->
      spec.json({
        context.render(json([error: true, message: ERROR_MSG]))
      }).html({
        context.render("<h1>400 Bad Request</h1><br/><div>${ERROR_MSG}</div>")
      }).noMatch {
        context.render(ERROR_MSG)
      }
    }
  }
}

ratpack {
  handlers {
    all(new UserAgentVersioningHandler()) // <3>

    get("api") { UserAgentVersioningHandler.ClientVersion clientVersion -> // <4>
      if (clientVersion == UserAgentVersioningHandler.ClientVersion.V1) {
        render "V1 Model"
      } else if (clientVersion == UserAgentVersioningHandler.ClientVersion.V2) {
        render "V2 Model"
      } else {             // it must be V3 at this point, as the versioning
        render "V3 Model"  // handler has figured out the request qualifies
      }
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
linux:~ # curl http://localhost:5050/api
linux:~ # curl -H "User-Agent: Microservice Client v1.0" http://localhost:5050/api
```