# hello


## command

```bash
linux:~ # python -c "print('Hello, Python')"
```

## interactive mode

```bash
linux:~ # python
```

## script

```python
#!/usr/bin/env python 

print('Hello, Python')
```

```bash
linux:~ # chmod u+x hello.py
linux:~ # ./hello.py
```

```bash
linux:~ # python hello.py
```

## environmental variable


| variable 			| description 												|
| --- 				| --- 														|
| PYTHONPATH 		| module path, 預設為 /usr/lib/python<version>/site-packages 	|
| PYTHONHOME 		| 模組搜尋路徑相關的變數, 預設為 /usr/lib/python<version> 		|
| PYTHONSTARTUP 	| interactive mode 所執行程式路徑 								|

---


# data type

## boolean


```bash
print(True, False)
print(1 == 1)
print(1 != 1)
print(1 > 1)
print(not True)
```

## string

```python
str1 = 'ABC' 
str2 = str1 
print("str1: ", str1, ", type: ", type(str1)) 		# string type and content
print(str1 == str2)

str1 = 'xyz'
print(str1 == str2)
print("str1 + str2: ", str1 + str2) 				# concat string


str3 = "ABC xyz 123\n" 								# string slice
print('str3[0]: ', str3[0], ', str3[-1]: ', str3[-1])
print('str3[:3]: ', str3[:3], ', str3[5:-1]: ', str3[5:-1])
print('str3[2:3:1]: ', str3[2:5:2])

print('str3.replace: ', str3.replace('123','456')) 	# replace string
print('str3.find: ', str3.find('xyz')) 				# find string
print("str3.split: ", str3.split(' ')) 				# string split to list
print("str3.rstrip: ", str3.rstrip()) 				# string strip
print(list(str3)) 									# string split to char


print("{}, {}!".format('Hi', 'Python')) 			# format output
```


## numeric

```python
# number type
print(type(1))
print(type(-2.1))
print(type(1 + 2j))

# number value
print(1)
print(-2.1)
print(1+2j)
print(0xff)
print(0o11)

print(int(1))
print(float(-2.1))
print(complex(1, 2))
print(hex(255))
print(oct(9))

# str convert to int
STR="123"
VAR=int(STR)
print("STR: ", STR, ", VAR: ", VAR)
print("STR type: ",type(STR), ", VAR type: ", type(VAR))
STR="456"
print("STR: ", STR, ", VAR: ", VAR)
```


## list

list 像是其他一般語言的陣列 (array) index 是從 0 開始, 但和 array 不一樣的, list 不需宣告型別, 可裝任何型別

list assign 時, 是 copy by reference 非 copy by value

```python
lst1 = [] 
print("LIST : ", lst1, ", LIST type: ", type(lst1))
lst1 = ["ABC", 'xyz', 123] 

lst2 = lst1 
lst3 = lst1[:] 
print("lst1: ", lst1, ", lst2: ", lst2, ", lst3: ", lst3)
lst1.append(45.7)
lst1.remove('ABC')
print("lst1: ", lst1, ", lst2: ", lst2, ", lst3: ", lst3)

for i in range(len(lst1)): 
    print("index: ", i, ", value: ", lst1[i])

for l in lst1: 
    print("value: ", l)


# string convert to list
print("XYZ, abc, 123".split(", "))

# list convert to string
print('. '.join(['123', "abc", 'XYZ']))


# 2D list
my_list1 = [] 
for x in range(5): 
    tmp_list = [] 
    for y in range(3): 
        tmp_list.append(None) 
    my_list1.append(tmp_list) 
print(my_list1)

# 使用 List Comprehensions 
my_list2 = [[None for _ in range(3)] for _ in range(5)] 
print(my_list2)

# 設定初始值不一樣的二維陣列 
my_list3 = [] 
for x in range(5): 
    tmp_list = [] 
    for y in range(3): 
        tmp_list.append(y + 3 * x) 
    my_list3.append(tmp_list) 
print(my_list3)

my_list4 = [[x + 3 * y for x in range(3)] for y in range(5)] 
print(my_list4)
print(my_list4[3][2])

# example
m = 4
n = 2

list1 = []
for i in range(n):
    list1.append(i)
print(list1, list1[1])

list1 = [i for i in range(n)]
print(list1)

list2 = []
for i in range(n):
    for j in range(m):
        list2.append(j + i * m)
print(list2)

list2 = [j + i * m for i in range(n) for j in range(m)]
print(list2)

list3 = []
for i in range(n):
    tmp = []
    for j in range(m):
        tmp.append(j + i * m)
    list3.append(tmp)
print(list3)

list3 = [[j + i * m for j in range(m)] for i in range(n)]
print(list3)
```


## dictionary

```python
dict1 = {} 
print("DICTIONARY: ", dict1, "DICTIONARY type: ",type(dict1))

dict1 = {'A': 'ABC', "x": "xyz", "0": 123} 
dict2 = dict1
print("dict1: ", dict1, "dict2: ", dict2)
print(dict1 == dict2)

# get key and value
print("dict1['A']: ", dict1['A'])
print("dict1['A']: ", dict1.get('A'))
print("dict1['test']: ", dict1.get('test', 'default'))
print(dict1 == dict2)

# add key and value
dict1['G'] = 'A2x'
dict1.update({'4': 45.7})
print(dict1)

# remove key and. value
del(dict1['x'])
dict1.pop('A')
print("dict1: ", dict1)


for key in dict1.keys(): 
    print("key: ", key, "value: ", dict1[key])

for key in dict1.keys(): 
    print("key: ", key, "value: ", dict1[key])

hoilday = {'sat': 'Saturday', 'sun': 'Sunday'}

print('sun' in hoilday.keys()) 	# check Key
print('sun' in hoilday) 		# check Key
```


## tuple

```python

# tuple 的顯示方式 
tup = (1, "xyz", 'ABC') 
for t in tup:
    print (t)

# net tuple 的使用方式 
h2o =((0, 0), (0, 1), (1, 0)) 
for atom in h2o:
    print (atom)

for x, y in h2o: 
    print (x, y)
```


## set

```python
set1 = {1, 2, 3}
print(type(set1))
print(set1)

set2 = {}
print(type(set2))

set3 = set()
set3.add(3)
print(type(set3))
print(set3)

print(set1 - set3)
```


## data time


---

# statement


## if else

python 只提供 if else 判斷, 使用方式如下, 但有些時候會想使用 switch case 方式作條件式的判斷, 但 python 本身無此功能, 只能使用 elif 方式

```bash
sex = input('input your sex [m/f]: ') 
if sex == 'm': 
    print('Male')
elif sex == 'f': 
    print('Female')
else: 
    print('Unknown')

# 使用 dictionary 方法替代 switch/case 
sex = {'m': 'Male', 'f': 'Female'} 
print(sex.get('m', 'Unknown'))
```

當 statement 只有一行, 可以使用下面方式

```python
import platform 

if platform.system() == "Linux": 
    OS = "Linux" 
else: 
    OS = "Unknown" 
print(OS)

# 另一種簡單方式的 if else 使用方式 
OS = "Linux" if platform.system() else "Unknown" 
print (OS)
```

and, or, not 的使用

```python
import os 

#兩個condition同時判斷檔案是否存在 
if os.path.exists(os.path.join(os.getenv('HOME'), '.profile') ) or os.path.exists(os.path.join(os.getenv('HOME'), '.bash_profile') ) : 
    print ".profile or .bashrc_profile exist"
```


## for

```python
list1 = ["ABC", 'xyz', 123] 
# 顯示l ist 內容 
for l in list1: 
    print(l)

dict1 = {"A":"ABC", 'b':"xyz", "0":123} 
# 顯示dictionary內容 
for D in dict1.keys(): 
    print(dict1[D])

# 數值迴圈的使用方式 
for i in range (5): 
    print(i)
```


## list comprehension

```python
lines1 = []
for line in open('/etc/passwd'):
    lines1.append(line.rstrip())
f.close() 
print(lines1)

lines2 = [line.rstrip() for line in open('/etc/passwd')] 
print(lines2)

lines1 == lines2
```

配合 if

```python
S = [x**2 for x in range(10)] 
V = [2**i for i in range(13)] 
M = [x for x in S if x % 2 == 0] 
print(S)
print(V)
print(M)

noprimes = [j for i in range(2, 8) for j in range(i*2, 50, i)] 
primes = [x for x in range(2, 50) if x not in noprimes] 
print(primes)
```


## while

```
import sys 

print("Input the word, [Quit]")
input1 = sys.stdin.readline().rstrip() 

while input1 != "Quit": 
    print("Your keyin: ", input1)
    input1 = sys.stdin.readline().rstrip()
```

```python
while True:
    word = input('Input the word, [Quit]')
    if word.lower() == 'quit':
        break
    elif word == '\n':
        continue
    else:
        print(word)
```


---

# function

## def

```bash
linux:~ # cat myswap01.py
def change(arg1, arg2):             # define function
    print("before: arg1: ", arg1, "arg2: ", arg2)
    (arg1, arg2) = (arg2 ,arg1)
    print("after: arg1: ", arg1, "arg2: ", arg2)
    return (arg1, arg2)             # return value

if __name__ == "__main__":          # define main function
    change("A", "B")

linux:~ # cat mymain01.py
import sys 
# sys.path.append('modulepath')       # 指定 module path, 定義 sys.path 即可
import myswap01                     # 載入 myswap01.py, myswap01.py 和 mymain01.py 同資料夾或是定義在 PYTHONPATH 或 sys.path

if __name__ == "__main__": 
    A = 3 
    B = 1 
    print "A: ", A, ", B: ", B 
    (C, D) = myswap01.change(A, B)  # 使用 myswap01.py 裡的 chnage 函式
    print "A: ", A, ", B: ", B
    print "C: ", C, ", D: ", D
```


##  *args, **kwargs

```python
def person(name = "NoName", *desc , **data):    # name = "NoName" default value, *desc 是傳入 tuple, **data 則是傳入 dict 
    print ("Name: %s" %name) 
    for k in data.keys():
        print("%s: %s" %(k, data[k]))
    for s in desc:
        print(s)

if __name__ == "__main__": 
    myStory='''I'm student.
I live in Taiei.'''.split('\n')
    myData = {"sex":"female", "age":"15"} 

    person("May", *myStory, **myData)           # 參數使用方式
```


## lambda

```python
my_sum = lambda x, y: x + y 
print(my_sum(1, 3))

my_greater_than = lambda x, y: x if x > y else y 
print(my_greater_than(7, 3))

round_up = lambda x, y: int(x / y) + (x % y > 0)
round_down = lambda x, y: int(x / y)
round_half = lambda x, y: int(x / y + 0.5)
```

```python
x = 10
a = lambda y: x + y
x = 20
b = lambda y: x + y
a(10)
b(10)
```

```python
x = 10
a = lambda y, x=x: x + y
x = 20
b = lambda y, x=x: x + y
a(10)
b(10)
```


## decorator

`simple decorator`

```python
def greet(function): 
    print('Hello')
    return function 

def greet_someone1(someone): 
    print(someone)
greet_someone1 = greet(greet_someone1) 

@greet 
def greet_someone2(someone): 
    print(someone)

greet_someone1('John')
print(greet_someone1.__name__)
greet_someone2('Mary')
print(greet_someone2.__name__)
```

`decorator without argument`

```python
def greet(function): 
    def wrapper(name): 
        print('Hello')
        return function(name) 
    return wrapper 

def greet_someone1(someone): 
    print(someone)
greet_someone1 = greet(greet_someone1) 

@greet 
def greet_someone2(someone): 
    print(someone)

greet_someone1('John') 
print(greet_someone1.__name__)
greet_someone2('Mary') 
print(greet_someone2.__name__)
```

`decorator with argument`

```python
def greet(arg = 'Hello'):
    def decorator(function):
        def wrapper(name): 
            print(arg)
            return function(name) 
        return wrapper
    return decorator

@greet('Hi')
def greet_someone(someone):
    print(someone)

greet_someone('John') 
print(greet_someone.__name__)
greet_someone('Mary') 
print(greet_someone.__name__)
```

`functool decorator without argument`

```python
import functools

def greet(function): 
    @functools.wraps(function)
    def wrapper(name):
        print('Hello')
        return function(name)
    return wrapper

@greet
def greet_someone(someone):
    print(someone)

greet_someone('John')
print(greet_someone.__name__)
```

`functool decorator with argument`

```python
import functools

def greet(arg = 'Hello'):
    def decorator(function):
        @functools.wraps(function) 
        def wrapper(name): 
            print(arg)
            return function(name) 
        return wrapper
    return decorator

@greet()
def greet_someone(someone): 
    print(someone)

greet_someone('John') 
print(greet_someone.__name__)
```


## comment

```python
def add1(x, y):
    return x + y

def add2(x:int, y:int) -> int:
    return x + y
```


---

# object

## attr

```python
class Person:
    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

obj = Person('man')

print(dir(obj))

print([mthd for mthd in dir(obj) if callable(getattr(obj, mthd))])
print([mthd for mthd in dir(obj) if callable(getattr(obj, mthd)) and not mthd.startswith("__")])

print([attr for attr in vars(obj)])
print(vars(obj))
print(obj.__dict__)
```


## class

```python
class Animal:
    def __init__(self, name=None):
        self.__name = name
        self.__voice = 'a'
        self.__age = 0
        self.__sex = 'unknown'
        print("Construct Animal")

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def set_age(self, age):
        self.__age = age

    def get_age(self):
        return self.__age

    age = property(get_age, set_age, 'age')

    @property
    def sex(self):
        return self.__sex

    @sex.setter
    def sex(self, sex):
        if sex.lower() == 'male' or sex.lower() == 'female':
            self.__sex = sex
        else:
            raise ValueError('Error sex value')

    @property
    def voice(self):
        return self.__voice

    def _set_voice(self, voice):
        self.__voice = voice

animal = Animal('animal')
print(animal.get_name())

animal.set_age(1)
print(animal.age)

print(animal.sex)
```


## inheritance

```python
class Felidae(Animal):
    def __init__(self, name):
        Animal.__init__(self, name)
        print('Construct Felidae, and inheritance Animal')


class Cat(Felidae):
    def __init__(self, name):
        super().__init__(name)
        self._set_voice('Meow')
        print('Construct Cat')

    def __str__(self):
        return 'Cat: {}'.format(self.get_name())

felidae = Felidae('felidae')
print(felidae.get_name())

cat = Cat('kitty')
print(cat.get_name())
print(cat.voice)
print(cat)
```


## multi-inheritance

```python
class Bird(Animal):
    def __init__(self):
        Animal.__init__(self)
        print("Construct Bird, and inheritance Animal")

    def fly(self):
        print("Flying in sky")

    def eat(self):
        print('Eat meat and fish')

class Griffin(Felidae, Bird):
    def __init__(self, name):
        super().__init__(name)
        print("Construct Felidae and Bird, and inheritance Animal")

    def eat(self):
        super(Felidae, self).eat()

griffin = Griffin('griffin')
griffin.walk()
griffin.fly()
griffin.eat()
```


## abstract class

```python
import abc

class AbcCar(metaclass=abc.ABCMeta):
    def __init__(self, volume):
        self._set_gasoline_volume(volume)
        self._gasoline = 0.0

    def _set_gasoline_volume(self, volume):
        self._volume = volume

    def get_volume(self):
        return self._volume

    def add_gasoline(self, volume):
        if self._gasoline + volume > self._volume:
            raise RuntimeError('add too much gasoline, max %f'.format(self._volume))
        self._gasoline += volume

    @property
    def gasoline(self):
        return self._gasoline

    def run(self, mileage):
        raise NotImplementedError()

    @abc.abstractmethod
    def turbo(self, mileage):
        pass

class Car(AbcCar):
    def run(self, mileage):
        if self._gasoline - mileage * 0.1 > 0:
            self._gasoline -= mileage * 0.1

    def turbo(self, mileage):
        if self._gasoline - mileage * 0.2 > 0:
            self._gasoline -= mileage * 0.2

car = Car(10)
car.add_gasoline(10)
print(car.gasoline)

car.turbo(10)
print(car.gasoline)

car.run(10)
print(car.gasoline)
```


## staticmethod, classmethod

```python
class Date(object):
    def __init__(self, day=0, month=0, year=0):
        self.day = day
        self.month = month
        self.year = year

    @classmethod
    def from_string(cls, date_as_string):
        day, month, year = map(int, date_as_string.split('-'))
        date1 = cls(day, month, year)
        return date1

    @staticmethod
    def is_date_valid(date_as_string):
        day, month, year = map(int, date_as_string.split('-'))
        return day <= 31 and month <= 12 and year <= 3999

date2 = Date.from_string('11-09-2012')
print(date2.year, date2.day)

print(Date.is_date_valid('11-09-2012'))
```


---

# regex

## match

```python
import re 

str = '/usr/lib/python2.6/site-packages/gtk-2.0/gconf.so'
print str 


# same as sh ${STR%.*} 
restr = re.compile('(.*)\.(.*?)$').match(str)
print("%s <=> %s" %(restr.group(1), restr.group(2)))
print(restr.group(1, 2))                                    # return list
print(restr.groups())                                       # same as above
print(re.sub('.[^.]*$', '', str))


# same as sh ${STR%%.*} 
restr = re.compile('(.*?)\.(.*)').match(str)
print("%s <=> %s" %(restr.group(1), restr.group(2)))
print(re.sub('\.(.*)', '', str))


# same as sh ${STR0#*/} 
restr = re.compile('(.*?)/(.*)').match(str)
print("%s <=> %s" %(restr.group(1), restr.group(2)))
print(re.sub('^(.*?)/', '', str))


# same as sh ${STR0##*/}
restr = re.compile('(.*)/(.*)').match(str)
print("%s <=> %s" %(restr.group(1), restr.group(2)))
print(re.sub('(.*)/', '', str))
```


## search

```python
import re

sentence = '''
wlan0 down AP wlan0 0 00:00:00:00:00:00 Wireless1
wlan1 down AP wlan1 0 00:00:00:00:00:00 Wireless2
wlan2 up AP wlan2 0 00:00:00:00:00:00 Wireless3
wlan36 up AP wlan36 1 00:00:00:00:00:00 Wireless13
wlan37 down AP wlan37 1 00:00:00:00:00:00 Wireless14
wlan38 up AP wlan38 1 00:00:00:00:00:00 Wireless15
wlan39 down AP wlan39 1 00:00:00:00:00:00 Wireless16
'''

lazy_pattern = 'wlan\d+.*up[\s\S]+?Wireless\d+'
greedy_pattern1 = 'wlan\d+.*up[\s\S]+Wireless\d+'
greedy_pattern2 = 'wlan\d+.*up[\s\S]*Wireless\d+'

lazy_match = re.search(lazy_pattern, sentence)
greedy_match1 = re.search(greedy_pattern1, sentence)
greedy_match2 = re.search(greedy_pattern2, sentence)
match_all = re.findall(lazy_pattern, sentence)

print("lazy:")
print(lazy_match.group())

print("greedy 1:")
print(greedy_match1.group())

print("greedy 2:")
print(greedy_match2.group())

print("find all:")
print(match_all)
```


---

# exception

## try, except, finally

```python
try: 
    a = int(input('input an integer number ')) 
    b = int(input('input an integer number ')) 
    if a > b: 
        print(n)
except ValueError: 
    print("Value Error, you don't input any character")
except: 
    print("Other Error")
else: 
    print("Normal finish")
finally: 
    print("force action")
```


## raise

```python
import math

anumber = int(input('input an integer number '))

if anumber < 0:
    raise RuntimeError("You can't use a negative number")
else:
    print(math.sqrt(anumber))
```


## defined exception

```python
class MyError(Exception): 
    def __init__(self, value): 
        self.value = value 

    def __str__(self): 
        return repr(self.value) 

try: 
    raise MyError(input("keyin any one: ")) 
except MyError as e: 
    print('My exception occurred, value:', e.value)
```


---

# format output

## old format

```python
print('%s' % 42)
print('%f' % 7.03)
print('%d%%' % 100)

print('this %s a %s test' % ('is', 'simple'))
```

## new format

```python
print('{},{},{}'.format('ecmadao', 'edward', 'cavalier'))
print('{2},{0},{1}'.format('ecmadao', 'edward', 'cavalier'))

example_dict = {'a': 0, 'b': 1, 'c': 2}
print('{a} {b} {c}'.format(a = 0, b = 1, c = 2))
print('{0[a]} {0[b]} {0[c]}{1}'.format(example_dict, 'others'))

print('{0: f}'.format(7.03))
```

## here document

```python
print('''hello python2
hi python3''')
```


---

# file

```python
f = open('/etc/passwd', 'r') 
lines1 = f.readlines() 
for line in lines1: 
    print(lines.rstrip())
f.close() 

with open('somefile.txt', 'w') as f:
    f.write('hello python')
```


---

# process

```python
import subprocess

subprocess.call(['ls', '-l'])

c1 = subprocess.Popen(['grep', '^root', '/etc/passwd'], stdout = subprocess.PIPE)
c2 = subprocess.Popen(["cut", "-d:", "-f1"], stdin = c1.stdout)
c2.communicate()
```

