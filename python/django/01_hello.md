# Django


----

## Hello Django

```
centos:~ # django-admin help

# Create project
centos:~ # django-admin startproject my_project
my_project/
├── manage.py
└── my_project
    ├── __init__.py
    ├── settings.py
    ├── urls.py
    └── wsgi.py

centos:~ # cd my_project

# Create app
centos:~/my_project # django-admin startapp my_app
my_app
├── __init__.py
├── admin.py
├── apps.py
├── migrations
│   └── __init__.py
├── models.py
├── tests.py
└── views.py

centos:~/my_project # vi my_project/settings.py
...
INSTALLED_APPS = [ 
...
    'my_app',
]
...

centos:~/my_project # vi my_project/urls.py
...
import my_app

urlpatterns = [ 
    path('admin/', admin.site.urls),
    path('hello/', my_app.views.hello),
    path('hi/', my_app.views.hi),
]

centos:~/my_project # vi my_app/views.py
from django.http import HttpResponse
from django.shortcuts import render

def hello(request):
    return HttpResponse('Hello Django')

def hi(request):
    return render(request, 'hi.html')

centos:~/my_project # mkdir -p my_app/templates
centos:~/my_project # vi my_app/templates/hi.html
Hi Django

centos:~/my_project # python manage.py runserver 0.0.0.0:8000
```

http://127.0.0.1:8000/hello

http://127.0.0.1:8000/hi
