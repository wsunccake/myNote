# Django


## Admin

```
centos:~/my_project # python manage.py migrate admin
centos:~/my_project # python manage.py migrate auth
centos:~/my_project # python manage.py migrate contenttypes
centos:~/my_project # python manage.py migrate sessions
centos:~/my_project # python manage.py createsuperuser --username admin --email admin@email.com

centos:~/my_project # vi my_app/admin.py
from django.contrib import admin
from my_app.models import Person

admin.site.register(Person)

centos:~/my_project # python manage.py runserver
```

http://127.0.0.1:8000/admin/
