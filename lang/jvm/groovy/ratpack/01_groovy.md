# Groovy

## Script

### Hello

```bash
linux:~ # cat app.groovy
@Grab('io.ratpack:ratpack-groovy:1.3.3')
import static ratpack.groovy.Groovy.ratpack

ratpack {
    handlers {
        get {
            render "Hello, Ratpack!"
        }
    }
}

linux:~ # groovy app.groovy

linux:~ # curl http://localhost:5050
```

### Path

```bash
linux:~ # cat app.groovy
@Grab('io.ratpack:ratpack-groovy:1.3.3')
import static ratpack.groovy.Groovy.ratpack

ratpack {
    handlers {
        path("foo") {
            byMethod {
//              http://localhost:5050/foo
                get {
                    render "Hello, Foo! Get"
                }

//              http://localhost:5050/foo/action -> 404
                get("action") {
                    render "Hello, Foo! Action"
                }

//              http://localhost:5050/foo
                post {
                    render "Hello, Foo! Post"
                }
            }
        }
    }
}

linux:~ # groovy app.groovy

linux:~ # curl http://localhost:5050/foo
linux:~ # curl -XPOST http://localhost:5050/foo
linux:~ # curl http://localhost:5050/foo/action
```

### Prefix

```bash
linux:~ # cat app.groovy
@Grab('io.ratpack:ratpack-groovy:1.3.3')
import static ratpack.groovy.Groovy.ratpack

ratpack {
    handlers {
        prefix("products") {
            get("list") {
                render "Product List"
            }

            get("get") {
                render "Product Get"
            }

            get("search") {
                render "Product Search"
            }
        }
    }
}

linux:~ # groovy app.groovy

linux:~ # curl http://localhost:5050/products/list
linux:~ # curl http://localhost:5050/products/get
linux:~ # curl http://localhost:5050/products/search
```


### Parameter

```bash
linux:~ # cat app.groovy
@Grab('io.ratpack:ratpack-groovy:1.3.3')
import static ratpack.groovy.Groovy.ratpack

ratpack {
    handlers {
        get("foo/:id?") {
            def name = pathTokens.id ?: "World"
            response.send "Hello $name!"
        }
    }
}

linux:~ # groovy app.groovy

linux:~ # curl http://localhost:5050/foo
linux:~ # curl http://localhost:5050/foo/kitty
```


### URL

```bash
linux:~ # cat app.groovy
@Grab('io.ratpack:ratpack-groovy:1.3.3')
import static ratpack.groovy.Groovy.ratpack

ratpack {
    handlers {
        get {
            def name = request.queryParams.name ?: "World"
            response.send "Hello, $name!"
        }
    }
}

linux:~ # groovy app.groovy

linux:~ # curl http://localhost:5050
linux:~ # curl http://localhost:5050?name=Kitty
```


### FORM

```bash
linux:~ # cat app.groovy
@Grab('io.ratpack:ratpack-groovy:1.3.3')
import static ratpack.groovy.Groovy.ratpack
import ratpack.form.Form

ratpack {
    handlers {
        all {
            byMethod {
                get {
                    response.send "text/html", """\
            <!DOCTYPE html>
            <html>
            <body>
            <form method="POST">
            <div>
            <label for="checked">Check</label>
            <input type="checkbox" id="checked" name="checked">
            </div>
            <div>
            <label for="name">Name</label>
            <input type="text" id="name" name="name">
            </div>
            <div>
            <input type="submit">
            </div>
            </form>
            </body>
            </html>
          """.stripIndent()
                }
                post {
                    parse(Form).then { formData ->
                        def msg = formData.checked ? "Thanks for the check!" : "Why didn't you check??"
                        response.send "text/html", """\
            <!DOCTYPE html>
            <html>
            <body>
            <h1>Welcome, ${formData.name ?: 'Guest'}!</h1>
            <span>${msg}</span>
            """.stripIndent()
                    }
                }
            }
        }
    }
}

linux:~ # groovy app.groovy

linux:~ # curl http://localhost:5050
```

### Header

```bash
linux:~ # cat app.groovy
@Grab('io.ratpack:ratpack-groovy:1.3.3')
import static ratpack.groovy.Groovy.ratpack
import static groovy.json.JsonOutput.toJson

class User {
    String username
    String email
}

def user1 = new User(username: "ratpack", email: "ratpack@ratpack.io")
def user2 = new User(username: "danveloper", email: "danielpwoods@gmail.com")
def users = [user1, user2]


ratpack {
    handlers {
        get("users") {
            byContent {
                html {
                    def usersHtml = users.collect { user ->
                        """\
                        |<div>
                        |<b>Username:</b> ${user.username}
                        |<b>Email:</b> ${user.email}
                        |</div>
                        """.stripMargin()
                    }.join()
                    render """\
                           |<!DOCTYPE html>
                           |<html>
                           |<head>
                           |<title>User List</title>
                           |</head>
                           |<body>
                           |<h1>Users</h1>
                           |${usersHtml}
                           |</body>
                           |</html>
                            """.stripMargin()
                }

                json {
                    render toJson(users)
                }

                xml {
                    def xmlStrings = users.collect { user ->
                        """
<user>
<username>${user.username}</username>
<email>${user.email}</email>
</user>
""".toString()
                    }.join()
                    render "<users>${xmlStrings}</users>"
                }

//curl -H "Accept: application/vnd.app.custom+json" http://localhost:5050/users
                type("application/vnd.app.custom+json") {
                    render toJson([
                            some_custom_data: "my custom data",
                            type: "custom-users",
                            users: users
                    ])
                }

//                noMatch {
//                    response.status 400
//                    render "negotiation not possible."
//                }

                noMatch "application/json"
            }
        }
    }
}


linux:~ # groovy app.groovy

linux:~ # curl http://localhost:5050/users
linux:~ # curl -H "Accept: application/json" http://localhost:5050/users
linux:~ # curl -H "Accept: application/xml" http://localhost:5050/users
linux:~ # curl -H "Accept: application/nothing" http://localhost:5050/users
```