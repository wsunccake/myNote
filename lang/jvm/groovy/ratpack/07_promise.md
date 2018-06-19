# Promise

## Java - General

```bash
linux:~ # mkdir project
linux:~ # cd project
linux:~/project # gradle init
linux:~/project # mkdir -p src/main/java/my/app
linux:~/project # vi src/main/java/my/app/Main.java
package my.app;

import ratpack.server.RatpackServer;
import java.lang.Exception;

public class Main {
  public static void main(String[] args) throws Exception {
    RatpackServer.start(spec -> spec
      .registryOf(r -> r
        .add(AsyncDatabaseService.class, new DemoAsyncDatabaseService())
        .add(new UserRenderer())
        .add(new UserProfileRenderer())
      )
      .handlers(chain -> chain
        .get(":username", ctx -> {
          AsyncDatabaseService db = ctx.get(AsyncDatabaseService.class);
          String username = ctx.getPathTokens().get("username");

          User user = db.findByUsername(username);
          ctx.render(user);
        })
        .prefix("profile", pchain -> pchain
          .get(":username", ctx -> {
            AsyncDatabaseService db = ctx.get(AsyncDatabaseService.class);
            String username = ctx.getPathTokens().get("username");

            User user = db.findByUsername(username);
            UserProfile profile = db.loadUserProfile(user.getProfileId());
            ctx.render(profile);
          })
        )
      )
    );
  }
}

linux:~/project # vi src/main/java/my/app/AsyncDatabaseService.java
package my.app;

import java.util.List;

public interface AsyncDatabaseService {
  User findByUsername(String username);
  UserProfile loadUserProfile(Long profileId);
}

linux:~/project # vi src/main/java/my/app/DemoAsyncDatabaseService.java
package my.app;

import java.util.function.Consumer;
import java.math.BigInteger;
import java.util.List;
import java.util.ArrayList;
import java.util.Arrays;

public class DemoAsyncDatabaseService implements AsyncDatabaseService {
  @Override
  public User findByUsername(String username) {
    User user = new User();
    try {
      Thread.sleep(200);
      user.setId(1l);
      user.setUsername(username);
      user.setProfileId(1l);
    } catch (Exception e) {
      System.out.println(e);
    }
    return user;
  }

  @Override
  public UserProfile loadUserProfile(Long profileId) {
    UserProfile profile = new UserProfile();
    try {
      Thread.sleep(200);
      profile.setId(profileId);
      profile.setUserId(1l);
      profile.setFirstName("Edgar");
      profile.setMiddleName("Allan");
      profile.setLastName("Poe");
    } catch (Exception e) {
      System.out.println(e);
    }
    return profile;
  }
}

linux:~/project # vi src/main/java/my/app/User.java
package my.app;

public class User {
  private Long id;
  private String username;
  private Long profileId;

  public Long getId() {
    return id;
  }

  public String getUsername() {
    return username;
  }

  public Long getProfileId() {
    return profileId;
  }

  public void setId(Long id) {
    this.id = id;
  }

  public void setUsername(String username) {
    this.username = username;
  }

  public void setProfileId(Long profileId) {
    this.profileId = profileId;
  }
}

linux:~/project # vi src/main/java/my/app/UserProfile.java
package my.app;

import java.util.List;

public class UserProfile {
  private Long id;
  private Long userId;
  private String username;
  private String firstName;
  private String middleName;
  private String lastName;
  private List<Long> friendIds;

  public Long getId() {
    return id;
  }

  public Long getUserId() {
    return userId;
  }

  public String getUsername() {
    return username;
  }

  public String getFirstName() {
    return firstName;
  }

  public String getMiddleName() {
    return middleName;
  }

  public String getLastName() {
    return lastName;
  }

  public void setId(Long id) {
    this.id = id;
  }

  public void setUserId(Long userId) {
    this.userId = userId;
  }

  public void setFirstName(String firstName) {
    this.firstName = firstName;
  }

  public void setMiddleName(String middleName) {
    this.middleName = middleName;
  }

  public void setLastName(String lastName) {
    this.lastName = lastName;
  }
}

linux:~/project # vi src/main/java/my/app/UserRenderer.java
package my.app;

import ratpack.render.Renderer;
import ratpack.handling.Context;
import java.lang.Exception;

import static ratpack.jackson.Jackson.json;

public class UserRenderer implements Renderer<User> {
  @Override
  public Class<User> getType() {
    return User.class;
  }

  @Override
  public void render(Context context, User user) throws Exception {
    context.render(json(user));
  }
}

linux:~/project # vi src/main/java/my/app/UserProfileRenderer.java
package my.app;

import ratpack.render.Renderer;
import ratpack.handling.Context;
import java.lang.Exception;

import static ratpack.jackson.Jackson.json;

public class UserProfileRenderer implements Renderer<UserProfile> {

  @Override
  public Class<UserProfile> getType() {
    return UserProfile.class;
  }

  @Override
  public void render(Context context, UserProfile profile) throws Exception {
    context.render(json(profile));
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

apply plugin: 'io.ratpack.ratpack-java'

repositories {
  jcenter()
}

mainClassName = "app.Main"

dependencies {
  runtime "org.slf4j:slf4j-simple:1.7.25"
}

linux:~/project # gradle run

linux:~ # curl http://localhost:5050/kitty
linux:~ # curl http://localhost:5050/profile/kitty
```

## Java - Promise

```bash
linux:~ # mkdir project
linux:~ # cd project
linux:~/project # gradle init
linux:~/project # mkdir -p src/main/java/my/app
linux:~/project # vi src/main/java/my/app/Main.java
package my.app;

import ratpack.server.RatpackServer;
import java.lang.Exception;

public class Main {

  public static void main(String[] args) throws Exception {
    RatpackServer.start(spec -> spec
      .registryOf(r -> r
        .add(AsyncDatabaseService.class, new DemoAsyncDatabaseService())
        .add(new UserRenderer())
        .add(new UserProfileRenderer())
      )
      .handlers(chain -> chain
        .get(":username", ctx -> {
          AsyncDatabaseService db = ctx.get(AsyncDatabaseService.class);
          String username = ctx.getPathTokens().get("username");
          db.findByUsername(username).then(user -> ctx.render(user));
        })
        .prefix("profile", pchain -> pchain
          .get(":username", ctx -> {
            AsyncDatabaseService db = ctx.get(AsyncDatabaseService.class);
            String username = ctx.getPathTokens().get("username");

            db.findByUsername(username).flatMap(user -> { 
              return db.loadUserProfile(user.getProfileId());
            }).then(profile -> { 
              ctx.render(profile);
            });
          })
        )
      )
    );
  }
}

linux:~/project # vi src/main/java/my/app/AsyncDatabaseService.java
package my.app;

import java.util.List;
import ratpack.exec.Promise;

public interface AsyncDatabaseService {
  Promise<User> findByUsername(String username);
  Promise<UserProfile> loadUserProfile(Long profileId);
}

linux:~/project # vi src/main/java/my/app/DemoAsyncDatabaseService.java
package my.app;

import java.util.function.Consumer;
import java.math.BigInteger;
import java.util.List;
import java.util.ArrayList;
import java.util.Arrays;
import ratpack.exec.Promise;

public class DemoAsyncDatabaseService implements AsyncDatabaseService {

  @Override
  public Promise<User> findByUsername(String username) {
    return Promise.async(down -> {
      new Thread(() -> {
        try {
          Thread.sleep(500);
          User user = new User();
          user.setId(1l);
          user.setUsername(username);
          user.setProfileId(1l);
          down.success(user);
        } catch (Exception e) {
          down.error(e);
        }
      }).start();
    });
  }

  @Override
  public Promise<UserProfile> loadUserProfile(Long profileId) {
    return Promise.async(down -> {
      new Thread(() -> {
        try {
          Thread.sleep(200);
          UserProfile profile = new UserProfile();
          profile.setId(profileId);
          profile.setUserId(1l);
          profile.setFirstName("Edgar");
          profile.setMiddleName("Allan");
          profile.setLastName("Poe");
          down.success(profile);
        } catch (Exception e) {
          down.error(e);
        }
      }).start();
    });
  }
}

linux:~/project # vi src/main/java/my/app/User.java
package my.app;

public class User {
  private Long id;
  private String username;
  private Long profileId;

  public Long getId() {
    return id;
  }

  public String getUsername() {
    return username;
  }

  public Long getProfileId() {
    return profileId;
  }

  public void setId(Long id) {
    this.id = id;
  }

  public void setUsername(String username) {
    this.username = username;
  }

  public void setProfileId(Long profileId) {
    this.profileId = profileId;
  }
}

linux:~/project # vi src/main/java/my/app/UserProfile.java
package my.app;

import java.util.List;

public class UserProfile {
  private Long id;
  private Long userId;
  private String username;
  private String firstName;
  private String middleName;
  private String lastName;
  private List<Long> friendIds;

  public Long getId() {
    return id;
  }

  public Long getUserId() {
    return userId;
  }

  public String getUsername() {
    return username;
  }

  public String getFirstName() {
    return firstName;
  }

  public String getMiddleName() {
    return middleName;
  }

  public String getLastName() {
    return lastName;
  }

  public void setId(Long id) {
    this.id = id;
  }

  public void setUserId(Long userId) {
    this.userId = userId;
  }

  public void setFirstName(String firstName) {
    this.firstName = firstName;
  }

  public void setMiddleName(String middleName) {
    this.middleName = middleName;
  }

  public void setLastName(String lastName) {
    this.lastName = lastName;
  }
}

linux:~/project # vi src/main/java/my/app/UserRenderer.java
package my.app;

import ratpack.render.Renderer;
import ratpack.handling.Context;
import java.lang.Exception;

import static ratpack.jackson.Jackson.json;

public class UserRenderer implements Renderer<User> {

  @Override
  public Class<User> getType() {
    return User.class;
  }

  @Override
  public void render(Context context, User user) throws Exception {
    context.render(json(user));
  }
}

linux:~/project # vi src/main/java/my/app/UserProfileRenderer.java
package my.app;

import ratpack.render.Renderer;
import ratpack.handling.Context;
import java.lang.Exception;

import static ratpack.jackson.Jackson.json;

public class UserProfileRenderer implements Renderer<UserProfile> {

  @Override
  public Class<UserProfile> getType() {
    return UserProfile.class;
  }

  @Override
  public void render(Context context, UserProfile profile) throws Exception {
    context.render(json(profile));
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

apply plugin: 'io.ratpack.ratpack-java'

repositories {
  jcenter()
}

mainClassName = "app.Main"

dependencies {
  runtime "org.slf4j:slf4j-simple:1.7.25"
}

linux:~/project # gradle run

linux:~ # curl http://localhost:5050/kitty
linux:~ # curl http://localhost:5050/profile/kitty
```

## Groovy - General

```bash
linux:~ # mkdir project
linux:~ # cd project
linux:~/project # gradle init
linux:~/project # mkdir -p src/ratpack
linux:~/project # vi src/ratpack/Ratpack.groovy
import static ratpack.groovy.Groovy.ratpack
import my.app.*

ratpack {
  bindings {
    bindInstance(AsyncDatabaseService.class, new DemoAsyncDatabaseService())
    bindInstance(new UserRenderer())
    bindInstance(new UserProfileRenderer())
  }  

  handlers {
    get {
      render "Hello Ratpack!"
    }

    get(":username") {
      AsyncDatabaseService db = get(AsyncDatabaseService.class)
      String username = getPathTokens().get("username")
      User user = db.findByUsername(username);
      render(user);
    }

    get("profile/:username"){
      AsyncDatabaseService db = get(AsyncDatabaseService.class)
      String username = getPathTokens().get("username")

      User user = db.findByUsername(username)
      UserProfile profile = db.loadUserProfile(user.getProfileId())
      render(profile)
    }
  }
}

linux:~/project # mkdir -p src/main/groovy/my/app

linux:~/project # vi src/main/groovy/my/app/AsyncDatabaseService.groovy
package my.app

import java.util.List

interface AsyncDatabaseService {
  User findByUsername(String username)
  UserProfile loadUserProfile(Long profileId)
}

linux:~/project # vi src/main/groovy/my/app/DemoAsyncDatabaseService.groovy
package my.app

import java.util.function.Consumer
import java.math.BigInteger
import java.util.List
import java.util.ArrayList
import java.util.Arrays

class DemoAsyncDatabaseService implements AsyncDatabaseService {
  @Override
  User findByUsername(String username) {
    User user = new User()
    try {
      Thread.sleep(200)
      user.setId(1l)
      user.setUsername(username)
      user.setProfileId(1l)
    } catch (Exception e) {
      System.out.println(e)
    }
    return user
  }

    @Override
    UserProfile loadUserProfile(Long profileId) {
    UserProfile profile = new UserProfile();
    try {
      Thread.sleep(200)
      profile.setId(profileId)
      profile.setUserId(1l)
      profile.setFirstName("Edgar")
      profile.setMiddleName("Allan")
      profile.setLastName("Poe")
    } catch (Exception e) {
      System.out.println(e)
    }
    return profile;
  }
}

linux:~/project # vi src/main/groovy/my/app/User.groovy
package my.app

class User {
  Long id
  String username
  Long profileId
}

linux:~/project # vi src/main/groovy/my/app/UserProfile.groovy
package my.app

import java.util.List

class UserProfile {
  Long id
  Long userId
  String username
  String firstName
  String middleName
  String lastName
  List<Long> friendIds
}

linux:~/project # vi src/main/groovy/my/app/UserRenderer.groovy
package my.app

import ratpack.render.Renderer
import ratpack.handling.Context
import java.lang.Exception

import static ratpack.jackson.Jackson.json

class UserRenderer implements Renderer<User> {
  @Override
  Class<User> getType() {
    return User.class
  }

  @Override
  void render(Context context, User user) throws Exception {
    context.render(json(user))
  }
}

linux:~/project # vi src/main/groovy/my/app/UserProfileRenderer.groovy
package my.app

import ratpack.render.Renderer
import ratpack.handling.Context
import java.lang.Exception

import static ratpack.jackson.Jackson.json

class UserProfileRenderer implements Renderer<UserProfile> {

  @Override
  Class<UserProfile> getType() {
    return UserProfile.class
  }

  @Override
  void render(Context context, UserProfile profile) throws Exception {
    context.render(json(profile))
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
  runtime "org.slf4j:slf4j-simple:1.7.25"
}

linux:~/project # gradle run

linux:~ # curl http://localhost:5050/kitty
linux:~ # curl http://localhost:5050/profile/kitty
```

## Groovy - Promise

```bash
linux:~ # mkdir project
linux:~ # cd project
linux:~/project # gradle init
linux:~/project # mkdir -p src/ratpack
linux:~/project # vi src/ratpack/Ratpack.groovy
import static ratpack.groovy.Groovy.ratpack
import my.app.*

ratpack {
  bindings {
    bindInstance(AsyncDatabaseService.class, new DemoAsyncDatabaseService())
    bindInstance(new UserRenderer())
    bindInstance(new UserProfileRenderer())
  }

  handlers {
    get {
      render "Hello Ratpack!"
    }

    get(":username") {
      AsyncDatabaseService db = get(AsyncDatabaseService.class)
      String username = getPathTokens().get("username")
      db.findByUsername(username).then({user ->
        render(user)
      })
    }

    get("profile/:username"){
      AsyncDatabaseService db = get(AsyncDatabaseService.class)
      String username = getPathTokens().get("username")
          
      db.findByUsername(username).flatMap({user ->  
        return db.loadUserProfile(user.getProfileId())
      }).then({profile ->
        render(profile)
      })
    }
  }
}

linux:~/project # mkdir -p src/main/groovy/my/app

linux:~/project # vi src/main/groovy/my/app/AsyncDatabaseService.groovy
package my.app

import java.util.List
import ratpack.exec.Promise

interface AsyncDatabaseService {
  Promise<User> findByUsername(String username)
  Promise<UserProfile> loadUserProfile(Long profileId)
}

linux:~/project # vi src/main/groovy/my/app/DemoAsyncDatabaseService.groovy
package my.app

import java.util.function.Consumer
import java.math.BigInteger
import java.util.List
import java.util.ArrayList
import java.util.Arrays
import ratpack.exec.Promise

class DemoAsyncDatabaseService implements AsyncDatabaseService {
  @Override
  Promise<User> findByUsername(String username) {
    return Promise.async({down ->
      User user = new User()
      try {
        Thread.sleep(200)
        user.setId(1l)
        user.setUsername(username)
        user.setProfileId(1l)
        down.success(user)
      } catch (Exception e) {
        down.error(e)
      }
      return user
    })
  }

  @Override
  Promise<UserProfile> loadUserProfile(Long profileId) {
    return Promise.async({down ->
      UserProfile profile = new UserProfile();
      try {
        Thread.sleep(200)
        profile.setId(profileId)
        profile.setUserId(1l)
        profile.setFirstName("Edgar")
        profile.setMiddleName("Allan")
        profile.setLastName("Poe")
        down.success(profile)
      } catch (Exception e) {
        down.error(e)
      }
      return profile
    })
  }
}

linux:~/project # vi src/main/groovy/my/app/User.groovy
package my.app

class User {
  Long id
  String username
  Long profileId
}

linux:~/project # vi src/main/groovy/my/app/UserProfile.groovy
package my.app

import java.util.List

class UserProfile {
  Long id
  Long userId
  String username
  String firstName
  String middleName
  String lastName
  List<Long> friendIds
}

linux:~/project # vi src/main/groovy/my/app/UserRenderer.groovy
package my.app

import ratpack.render.Renderer
import ratpack.handling.Context
import java.lang.Exception

import static ratpack.jackson.Jackson.json

class UserRenderer implements Renderer<User> {

  @Override
  Class<User> getType() {
    return User.class
  }

  @Override
  void render(Context context, User user) throws Exception {
    context.render(json(user))
  }
}

linux:~/project # vi src/main/groovy/my/app/UserProfileRenderer.groovy
package my.app

import ratpack.render.Renderer
import ratpack.handling.Context
import java.lang.Exception

import static ratpack.jackson.Jackson.json

class UserProfileRenderer implements Renderer<UserProfile> {

  @Override
  Class<UserProfile> getType() {
    return UserProfile.class
  }

  @Override
  void render(Context context, UserProfile profile) throws Exception {
    context.render(json(profile))
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
  runtime "org.slf4j:slf4j-simple:1.7.25"
}

linux:~/project # gradle run

linux:~ # curl http://localhost:5050/kitty
linux:~ # curl http://localhost:5050/profile/kitty
```

