# data type

---

## content

- [boolean](#boolean)
- [string](#string)
- [numeric](#numeric)
- [list](#list)
- [dictionary](#dictionary)
- [tuple](#tuple)
- [set](#set)
- [data time](#data-time)

---

## boolean

```bash
print(True, False)
print(1 == 1)
print(1 != 1)
print(1 > 1)
print(not True)
```

---

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

---

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

---

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

---

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

---

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

---

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

---

## data time
