# Django


----

## URL

```
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
    ...
    path('talk/<str:name>/', views.talk, name='talk'),
    re_path(r'^tell/(\S+)/$', views.tell, name='tell'),
]

centos:~/my_project # vi my_app/views.py
from django.shortcuts import render

def talk(request, name):
    return render(request, 'talk.html', {'user': name})

def tell(request, offset):
    return render(request, 'tell.html', {'user': offset})

centos:~/my_project # vi vi my_app/templates/say.html
Hi {{ user }}

centos:~/my_project # vi vi my_app/templates/fake_login.html
Hi {{ user }}<br>

centos:~/my_project # python manage.py shell
> from django.urls import reverse
> reverse('talk', args=['abc'])
> reverse('tell', args=['abc'])
```
