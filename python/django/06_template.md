# install django


----

## Template

```
centos:~/my_project # python manage.py shell
> from django import template
> t = template.Template('My name is {{ name }}.')
> c = template.Context({'name': 'Adrian'})
> print(c['name'])
> print(t.render(c))

> t = template.Template('{{ person.name.upper }} is {{ person.age }} years old.')
> person = {'name': 'Sally', 'age': '43'}
> c = template.Context({'person': person})
> print(t.render(c))

# split origin to base and other
centos:~/my_project # cat origin.html
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN">
<html lang="en">
<head>
    <title>The current time</title>
</head>
<body>
    <h1>My helpful timestamp site</h1>
    <p>It is now {{ current_date }}.</p>

    <hr>
    <p>Thanks for visiting my site.</p>
</body>
</html>

centos:~/my_project # cat base.html
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN">
<html lang="en">
<head>
    <title>{% block title %}{% endblock %}</title>
</head>
<body>
    <h1>My helpful timestamp site</h1>
    {% block content %}{% endblock %}
    {% block footer %}
    <hr>
    <p>Thanks for visiting my site.</p>
    {% endblock %}
</body>
</html>

centos:~/my_project # cat page.html
{% extends "base.html" %}

{% block title %}The current time{% endblock %}

{% block content %}
<p>It is now {{ current_date }}.</p>
{% endblock %}
```
