# install django


----

## ORM

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
    path('person_id/', views.person_id),
]

centos:~/my_project # vi my_app/models.py
from django.db import models

class Person(models.Model):
#    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    age = models.IntegerField()

centos:~/my_project # vi my_app/views.py
from django.http import HttpResponse
from my_app.models import Person

def person_id(request):
    user_id = int(request.GET.get('id', '1'))
    person = Person.objects.get(id=user_id)
    return HttpResponse('Hi {}'.format(person.name))

    def __str__(self):
        return self.name
```


### ORM operation

```
# Check orm
centos:~/my_project # python manage.py check

# Create/Update my_app/migration
centos:~/my_project # python manage.py makemigrations my_app

# Create/Update database
centos:~/my_project # python manage.py sqlmigrate my_app 0001
centos:~/my_project # python manage.py migrate my_app

sql>
CREATE TABLE person (
  id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  name varchar(20) NOT NULL,
  age integer NOT NULL
);

# Shell mode
centos:~/my_project # python manage.py shell

# ORM crud
> from my_app.models import Person
## Create
> p = Person(name='Ramesh', age=10)
> p.save()
> Person(name='Khilan', age=25).save()
> Person(name='Kaushik', age=23).save()
## Read
> Person.objects.all()
> Person.objects.get(id=1)
> Person.objects.filter(name__contains='ik')
> Person.objects.filter(age__lt=18)
## Update
> p = Person.objects.get(id=1)
> p.age = 11
> p.save()
> Person.objects.filter(id=1).update(age=11)
## Delete
> p = Person.objects.get(id=1)
> p.delete()
> Person.objects.filter(id=1).delete()
```


### 1 - 1

```
centos:~/my_project # vi my_app/models.py
class IdCard(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE, primary_key=True)
    number = models.CharField(max_length=20)

    def __str__(self):
        return self.number

# Run check orm, update my_app/mirgation and database
sql>
CREATE TABLE idcard (
  id integer NOT NULL PRIMARY KEY REFERENCES person (id) DEFERRABLE INITIALLY DEFERRED,
  number varchar(20) NOT NULL
);

# shell mode
centos:~/my_project # python manage.py shell
> from my_app.models import IdCard
> IdCard(person=p, number='A123').save()
```

### 1 - M

```
centos:~/my_project # vi my_app/models.py
class Phone(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    number = models.CharField(max_length=20)

    def __str__(self):
        return self.number

# Run check orm, update my_app/mirgation and database
sql>
CREATE TABLE phone (
  id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  number varchar(20) NOT NULL,
  person_id integer NOT NULL REFERENCES person (id) DEFERRABLE INITIALLY DEFERRED
);

# shell mode
centos:~/my_project # python manage.py shell
> from my_app.models import Phone
> Phone(person=p, number='123').save()
> Phone(person=p, number='567').save()
```

### M - M

```
centos:~/my_project # vi my_app/models.py
class Item(models.Model):
    person = models.ManyToManyField(Person)
    name = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.number

# Run check orm, update my_app/mirgation and database
sql>
CREATE TABLE item (
  id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  name varchar(20) NOT NULL,
  price decimal NOT NULL
);

sql>
CREATE TABLE "my_app_item_person" (
  id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  item_id integer NOT NULL REFERENCES item (id) DEFERRABLE INITIALLY DEFERRED,
  person_id integer NOT NULL REFERENCES person (id) DEFERRABLE INITIALLY DEFERRED
);

# shell mode
centos:~/my_project # python manage.py shell
> from my_app.models import Item
> i = Item(name='watch', price=10)
> i.person.add(p)
> i.person.all()
```
