# Basic

## Hello

`code`

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
```


`run`

```bash
linux:~ # groovy app.groovy
```

`test`

```
linux:~ # curl http://localhost:5050
```
