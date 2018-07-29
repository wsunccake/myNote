# Header

`code`

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
```

`test`

```bash
linux:~ # curl http://localhost:5050/users
linux:~ # curl -H "Accept: application/json" http://localhost:5050/users
linux:~ # curl -H "Accept: application/xml" http://localhost:5050/users
linux:~ # curl -H "Accept: application/nothing" http://localhost:5050/users
```