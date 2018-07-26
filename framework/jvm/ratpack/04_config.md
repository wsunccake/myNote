# Config

## File, Environment, Property

```bash
linux:~ # mkdir project
linux:~ # cd project
linux:~/project # gradle init
linux:~/project # mkdir -p src/ratpack
linux:~/project # vi src/ratpack/Ratpack.groovy
import static ratpack.groovy.Groovy.ratpack
import static groovy.json.JsonOutput.toJson
import java.nio.file.Paths

class DatabaseConfig {
  String host = "localhost"
  String user = "root"
  String password
  String db = "myDB"
}

ratpack {
  serverConfig {
    json Paths.get("/etc/dbconfig.json")
    json Class.getResource("/config/dbconfig.json") // in Jar
    json "dbconfig.json"
    yaml "dbconfig.yml"
    env()
    sysProps()
    require("/database", DatabaseConfig)
  }
  handlers {
    get("config") { DatabaseConfig config ->
      render toJson(config)
    }
  }
}

linux:~/project # vi src/ratpack/dbconfig.json
{
  "database": { 
    "host": "json.db",
    "user": "json",
    "password": "R@tpack"
  }
}

linux:~/project # vi src/ratpack/dbconfig.yml
database:
    host: yml.db
    user: yml
    password: R@tpack

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

run {
  systemProperties System.getProperties()
}

linux:~/project # gradle run
linux:~/project # env RATPACK_DATABASE__HOST=env.db ./gradlew run
linux:~/project # gradle -Dratpack.database.host=pros.db run

linux:~ # curl http://localhost:5050/config
```

## Nested Config

## Custom Config
