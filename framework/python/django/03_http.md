# install django


----

## Http Method

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
    path('say/', views.say),
    path('fake_login/', views.fake_login),
]

centos:~/my_project # vi my_app/views.py
from django.shortcuts import render

def say(request):
    return render(request, 'say.html', {'user': request.GET.get('name', 'Django')})

def fake_login(request):
    message = ''
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST['password']

        if (username == 'admin') and (password == '1234'):
            message = 'login success'
        else:
            message = 'login fail'

    return render(request, 'fake_login.html', {'message': message})

centos:~/my_project # vi vi my_app/templates/say.html
Hi {{ user }}

centos:~/my_project # vi vi my_app/templates/fake_login.html
{{ message }}<br>

<h2>Login</h2>
<form method="post">
    username: <input type="text" name="username"><br>
    password: <input type="password" name="password"><br>
    <input type="submit" value="Submit">
    {% csrf_token %}
</form>
```
