# Template Engines


## Markup Template Engine

```groovy
import groovy.text.*
import groovy.text.markup.*

MarkupTemplateEngine engine = new MarkupTemplateEngine(new TemplateConfiguration())

Template template = engine.createTemplate('''
html(lang:'en') {
    head {
        meta('http-equiv':'"Content-Type" content="text/html; charset=utf-8"')
        title('My page')
    }
    body {
        p('Hello Markup Template Engine')
    }
}
''')

println template.make([:])
```


---

## Layout

`tpl`

```tpl
html {
    head {
        title(title)                
    }
    body {
        bodyContents()              
    }
}
```

`groovy`

```groovy
import groovy.text.*
import groovy.text.markup.*

MarkupTemplateEngine engine = new MarkupTemplateEngine(new TemplateConfiguration())

Template template = engine.createTemplate('''
layout 'layout-main.tpl',
    true,
    title: 'Layout example',
    bodyContents: contents { p('This is the body') }   
''')

println template.make([:])
```

```groovy
import groovy.text.*
import groovy.text.markup.*

MarkupTemplateEngine engine = new MarkupTemplateEngine(new TemplateConfiguration())

Template template = engine.createTemplate('''
layout 'layout-main.tpl',
    true,
    bodyContents: contents { p('This is the body') }
''')

model = new HashMap<String,Object>();
model.put('title','Title from main model');

println template.make(model)
```


---

## Rendering

```bash
linux:~ # vi layout-main.tpl
html {
    head {
        title(title)                
    }
    body {
        bodyContents()              
    }
}

linux:~ # vi example.groovy
import groovy.text.*
import groovy.text.markup.*

TemplateConfiguration config = new TemplateConfiguration()
MarkupTemplateEngine engine = new MarkupTemplateEngine(config)
Template template = engine.createTemplateByPath('layout-main.tpl')

model = new HashMap<>()
model.put('title','Title from main model')

println template.make(model)
```


---

## Config

```tpl
html {
    body {
        div(unescaped.unsafeContents)
    }
}
```

```groovy
import groovy.text.*
import groovy.text.markup.*

TemplateConfiguration config = new TemplateConfiguration()
config.setAutoNewLine(true)
config.setAutoIndent(true)
MarkupTemplateEngine engine = new MarkupTemplateEngine(config)
Template template = engine.createTemplateByPath('main.tpl')

model = new HashMap<>()
model.put('title','Title from main model')

println template.make(model)
```

`config.setAutoEscape(false)`

```groovy
model.put("unsafeContents", "I am an <html> hacker.")
```

=>

```html
<html><body><div>I am an <html> hacker.</div></body></html>
```

`config.setAutoEscape(false)`

```groovy
model.put("unsafeContents", "I am an <html> hacker.")
```

=>

```html
<html><body><div>I am an &lt;html&gt; hacker.</div></body></html>
```


---

```tpl
p {
    yield "This is a "
    a(href:'target.html', "link")
    yield " to another page"
}
```

```tpl
p {
    yield "This is a ${a(href:'target.html', "link")} to another page"
}
```

---

## Reference

[Template engines](http://docs.groovy-lang.org/next/html/documentation/template-engines.html)

[Using the innovative Groovy template engine in Spring Boot](https://spring.io/blog/2014/05/28/using-the-innovative-groovy-template-engine-in-spring-boot)

[Spring Boot and Groovy Tutorial](https://o7planning.org/en/11799/spring-boot-and-groovy-tutorial)

[Spring Boot - Using Groovy View](https://www.logicbig.com/tutorials/spring-framework/spring-boot/groovy-view.html)

