# Data

## form

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
```

`test`

```
linux:~ # curl http://localhost:5050
linux:~ # curl --request POST --form age=10 http://localhost:5050/hello/test   
```


---

## json

```bash
linux:~ # vi app.groovy
@Grab('io.ratpack:ratpack-groovy:1.3.3')
import static ratpack.groovy.Groovy.ratpack
import groovy.json.JsonOutput
import groovy.json.JsonSlurper

JsonSlurper jsonSlurper = new JsonSlurper()

ratpack {
    handlers {
        path('api') {
            byMethod {
                post {
                    request.body.map {body ->
                        jsonSlurper.parseText(body.text) as Map
                    }.then { data ->
                        data << ['id': '1']
                        response.send(JsonOutput.toJson(data))
                    }
                }
            }
        }
    }
}
```

`test`

```bash
linux:~ # curl --request POST --data '{"name": "Ratpack"}' http://localhost:5050/api  
```
