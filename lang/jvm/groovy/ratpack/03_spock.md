# Spock

## Simple

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
      render "Hello Ratpack!"
    }
  }
}

linux:~/project # mkdir -p src/main/groovy/my/app
linux:~/project # vi src/main/groovy/my/app/MyService.groovy
package my.app

class MyService {

  String doServiceCall() {
    "service was called"
  }

  void shutdown() {
    // stub implementation
  }
}

linux:~/project # mkdir -p src/test/groovy/my/app
linux:~/project # vi src/test/groovy/my/app/MyServiceSpec.groovy
package my.app

import spock.lang.Specification

class MyServiceSpec extends Specification {

  void "service calls should return proper response"() {
    setup:
    "Set up the service for testing"
    def service = new MyService()

    when:
    "Perform the service call"
    def result = service.doServiceCall()

    then:
    "Ensure that the service call returned the proper result"
    result == "service was called"

    cleanup:
    "Shutdown the service when this feature is complete"
    service.shutdown()
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

dependencies {
  testCompile ratpack.dependency('test')
  testCompile 'org.spockframework:spock-core:1.0-groovy-2.4'
  testCompile 'cglib:cglib:2.2.2'
  testCompile 'org.objenesis:objenesis:2.1'
}

linux:~/project # gradle test
```

## Functional Test

```bash
linux:~ # mkdir project
linux:~ # cd project
linux:~/project # gradle init
linux:~/project # mkdir -p src/main/java/my/app
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

linux:~/project # mkdir -p src/test/groovy/my/app
linux:~/project # vi src/test/groovy/my/app/FunctionalSpec.groovy
package my.app

import ratpack.test.MainClassApplicationUnderTest
import spock.lang.Specification

class FunctionalSpec extends Specification {

  void "default handler should render Hello Ratpack!"() {
    setup:
    def aut = new MainClassApplicationUnderTest(Main)

    when:
    def response = aut.httpClient.text

    then:
    response == "Hello Ratpack!"

    cleanup:
    aut.close()
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
apply plugin: 'io.ratpack.ratpack-groovy'
apply plugin: "idea"

repositories {
  jcenter()
}

dependencies {
  runtime "org.slf4j:slf4j-simple:1.7.25"
  testCompile ratpack.dependency('test')
  testCompile 'org.spockframework:spock-core:1.0-groovy-2.4'
  testCompile 'cglib:cglib:2.2.2'
  testCompile 'org.objenesis:objenesis:2.1'
}

mainClassName = "my.app.Main"

linux:~/project # gradle test
```

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
    def userAgent = context.request.headers.get("User-Agent")
    def clientVersion = ClientVersion.fromString(userAgent)
    if (!clientVersion) {
      renderError(context)
    } else {
      context.next(Registry.single(ClientVersion, clientVersion))
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
    all(new UserAgentVersioningHandler())

    get("api") { UserAgentVersioningHandler.ClientVersion clientVersion ->
      if (clientVersion == UserAgentVersioningHandler.ClientVersion.V1) {
        render "V1 Model"
      } else if (clientVersion == UserAgentVersioningHandler.ClientVersion.V2) {
        render "V2 Model"
      } else {
        render "V3 Model"
      }
    }
  }
}

linux:~/project # mkdir -p src/test/groovy/my/app
linux:~/project # vi src/test/groovy/my/app/MultiSpec.groovy
import ratpack.groovy.test.GroovyRatpackMainApplicationUnderTest
import spock.lang.AutoCleanup
import spock.lang.Specification

class MultiSpec extends Specification {

  @AutoCleanup
  def aut = new GroovyRatpackMainApplicationUnderTest()

  void "should properly render for v1.0 clients"() {
    when:
    def response = aut.httpClient.requestSpec { spec ->
      spec.headers.'User-Agent' = ["Microservice Client v1.0"]
    }.get("api").body.text

    then:
    response == "V1 Model"
  }

  void "should properly render for v2.0 clients"() {
    when:
    def response = aut.httpClient.requestSpec { spec ->
      spec.headers.'User-Agent' = ["Microservice Client v2.0"]
    }.get("api").body.text

    then:
    response == "V2 Model"
  }

  void "should properly render for v3.0 clients"() {
    when:
    def response = aut.httpClient.requestSpec { spec ->
      spec.headers.'User-Agent' = ["Microservice Client v3.0"]
    }.get("api").body.text

    then:
    response == "V3 Model"
  }
}

linux:~/project # vi src/test/groovy/my/app/RollupsSpec.groovy
import ratpack.groovy.test.GroovyRatpackMainApplicationUnderTest
import spock.lang.AutoCleanup
import spock.lang.Specification
import spock.lang.Unroll

class RollupsSpec extends Specification {

  @AutoCleanup
  def aut = new GroovyRatpackMainApplicationUnderTest()

  @Unroll
  void "should render #expected for #userAgent clients"() {
    when:
    def response = aut.httpClient.requestSpec { spec ->
      spec.headers.'User-Agent' = [userAgent]
    }.get("api").body.text

    then:
    response == expected

    where:
    userAgent                  | expected
    "Microservice Client v1.0" | "V1 Model"
    "Microservice Client v2.0" | "V2 Model"
    "Microservice Client v3.0" | "V3 Model"
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

dependencies {
  testCompile ratpack.dependency('test')
  testCompile 'org.spockframework:spock-core:1.0-groovy-2.4'
  testCompile 'cglib:cglib:2.2.2'
  testCompile 'org.objenesis:objenesis:2.1'
}

linux:~/project # gradle test
```

## Blocking

```bash
linux:~ # mkdir project
linux:~ # cd project
linux:~/project # gradle init
linux:~/project # mkdir -p src/ratpack
linux:~/project # vi src/ratpack/Ratpack.groovy
import groovy.json.JsonSlurper

import static groovy.json.JsonOutput.toJson
import static ratpack.groovy.Groovy.ratpack

class User {
  String username
  String email
}

List<User> userStorage = []
JsonSlurper jsonSlurper = new JsonSlurper()

ratpack {

  handlers {
    path("api") {
      byMethod {
        post {
          request.body.map { body ->
            jsonSlurper.parseText(body.text) as Map
          }.map { data ->
            new User(data)
          }.then { user ->
            userStorage << user
            response.send()
          }
        }
        get {
          response.send(toJson(userStorage))
        }
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

linux:~ # curl http://localhost:5050/api
linux:~ # curl -XPOST -d '{"username": "kitty", "email": "kitty@mail.com"}' http://localhost:5050/api
linux:~ # curl http://localhost:5050/api
```

## Non Blocking

```bash
linux:~ # mkdir project
linux:~ # cd project
linux:~/project # gradle init
linux:~/project # mkdir -p src/ratpack
linux:~/project # vi src/ratpack/Ratpack.groovy
import my.app.DefaultUserService
import my.app.User
import my.app.UserService
import groovy.json.JsonSlurper

import static groovy.json.JsonOutput.toJson
import static ratpack.groovy.Groovy.ratpack

ratpack {
  bindings {
    bindInstance UserService, new DefaultUserService()
    bindInstance JsonSlurper, new JsonSlurper()
  }
  handlers {
    path("api") { JsonSlurper jsonSlurper, UserService userService ->
      byMethod {
        post {
          request.body.map { body ->
            jsonSlurper.parseText(body.text) as Map
          }.map { data ->
            new User(data)
          }.flatMap { user ->
            userService.save(user)
          }.then {
            response.send()
          }
        }
        get {
          userService.getUsers().then { users ->
            response.send(toJson(users))
          }
        }
      }
    }
  }
}

linux:~/project # mkdir -p src/main/groovy/my/app
linux:~/project # vi src/main/groovy/my/app/User.groovy
package my.app

class User {
  String username
  String email
}

linux:~/project # vi src/main/groovy/my/app/UserService.groovy
package my.app

import ratpack.exec.Promise

interface UserService {
  Promise<Void> save(User user)
  Promise<List<User>> getUsers()
}

linux:~/project # vi src/main/groovy/my/app/DefaultUserService.groovy
package my.app

import ratpack.exec.Promise

class DefaultUserService implements UserService {
  private final List<User> storage = []

  @Override
  Promise<Void> save(User user) {
    storage << user
    Promise.sync { null }
  }

  Promise<List<User>> getUsers() {
    Promise.sync { storage }
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

dependencies {
  testCompile ratpack.dependency('test')
  testCompile 'org.spockframework:spock-core:1.0-groovy-2.4'
  testCompile 'cglib:cglib:2.2.2'
  testCompile 'org.objenesis:objenesis:2.1'
}

dependencies {
  testCompile ratpack.dependency('test')
  testCompile 'org.spockframework:spock-core:1.0-groovy-2.4'
  testCompile 'cglib:cglib:2.2.2'
  testCompile 'org.objenesis:objenesis:2.1'
}

linux:~/project # gradle run

linux:~ # curl http://localhost:5050/api
linux:~ # curl -XPOST -d '{"username": "kitty", "email": "kitty@mail.com"}' http://localhost:5050/api
linux:~ # curl http://localhost:5050/api
```

### Funtional Test

```bash
linux:~/project # mkdir -p src/test/groovy/my/app
linux:~/project # vi src/test/groovy/my/app/FunctionalSpec.groovy
package my.app

import groovy.json.JsonSlurper
import ratpack.groovy.test.GroovyRatpackMainApplicationUnderTest
import spock.lang.AutoCleanup
import spock.lang.Specification

import static groovy.json.JsonOutput.toJson

class FunctionalSpec extends Specification {

  private static final JsonSlurper jsonSlurper = new JsonSlurper()

  @AutoCleanup
  def aut = new GroovyRatpackMainApplicationUnderTest()

  void "bootstrap data and properly render it back"() {
    setup:
    def user = [username: "kitty", email: "kitty@gmail.com"]

    when:
    def response = aut.httpClient.requestSpec { spec ->
      spec.body { b ->
        b.text(toJson(user))
      }
    }.post('api')

    then:
    response.statusCode == 200

    when:
    def json = aut.httpClient.get('api').body.text

    and:
    def users = jsonSlurper.parseText(json) as List

    then:
    users == [user]
  }
}

linux:~/project # gradle test
```

### Integration Test

```bash
linux:~/project # mkdir -p src/test/groovy/my/app
linux:~/project # vi src/test/groovy/my/app/IntegrationSpec.groovy
package my.app

import ratpack.exec.Promise
import ratpack.registry.Registry
import ratpack.groovy.test.GroovyRatpackMainApplicationUnderTest
import ratpack.impose.ImpositionsSpec
import ratpack.impose.UserRegistryImposition
import spock.lang.AutoCleanup
import spock.lang.Specification

import static groovy.json.JsonOutput.toJson

class IntegrationSpec extends Specification {
  UserService mockUserService = Mock(UserService)

  @AutoCleanup
  def aut = new GroovyRatpackMainApplicationUnderTest() {
    @Override
    protected void addImpositions(ImpositionsSpec impositions) {
      impositions.add(UserRegistryImposition.of(
        Registry.of { r ->
          r.add(UserService, mockUserService)
        }
      ))
    }
  }

  void "should convert and save user data"() {
    setup:
    def userMap = [username: "kitty", email: "kitty@mail.com"]

    when:
    aut.httpClient.requestSpec { spec ->
      spec.body { b ->
        b.text(toJson(userMap))
      }
    }.post('api')

    then:
    1 * mockUserService.save(_) >> { User user ->
      assert user.email == userMap.email
      assert user.username == userMap.username
      Promise.sync { null }
    }
  }

  void "should render user list as json"() {
    setup:
    def users = [
        new User(username: "kitty", email: "kitty@mail.com"),
        new User(username: "daniel", email: "daniel@mail.com"),
        new User(username: "ratpack", email: "ratpack@mail.com")
    ]

    when:
    def response = aut.httpClient.get("api")

    then:
    1 * mockUserService.getUsers() >> Promise.sync { users }
    response.body.text == toJson(users)
  }
}

linux:~/project # gradle test
```

### Unit Test

```bash
linux:~/project # mkdir -p src/test/groovy/my/app
linux:~/project # vi src/test/groovy/my/app/UserServiceUnitSpec.groovy
package my.app

import ratpack.test.exec.ExecHarness
import spock.lang.AutoCleanup
import spock.lang.Shared
import spock.lang.Specification
import spock.lang.Subject

class UserServiceUnitSpec extends Specification {
  private static final def users = [
      new User(username: "kitty", email: "kitty@mail.com"),
      new User(username: "daniel", email: "daniel@main.com"),
      new User(username: "ratpack", email: "ratpack@mail.com")
  ]

  @AutoCleanup
  ExecHarness execHarness = ExecHarness.harness()

  @Subject @Shared
  UserService userService = new DefaultUserService()

  void "should save and return user list"() {
    given:
    execHarness.yield {
      users.each { user -> userService.save(user) }
    }

    expect:
    execHarness.yieldSingle {
      userService.getUsers()
    }.value == users
  }
}

linux:~/project # gradle test
```