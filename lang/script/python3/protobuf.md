# protocol buffers 3

## package

```bash
linux:~ # wget https://github.com/protocolbuffers/protobuf/releases/download/v3.0.0/protoc-3.0.0-linux-x86_64.zip
linux:~ # unzip -l protoc-3.0.0-linux-x86_64.zip
linux:~ # unzip protoc-3.0.0-linux-x86_64.zip bin/protoc -d /usr/local/pkg/protoc
linux:~ # ln -s /usr/local/pkg/protoc/bin/protoc /usr/local/bin/.
```


---

## test

```bash
linux:~ # pip install protobuf

linux:~ # protoc --python_out=. *.proto
linux:~ # ls -l user_pb2.py

linux:~ # ipython
> import user_pb2
> u = user_pb2.User()
> u.id = 1
> u.age =12
> u.name ='john'
> u
```


---

## example

```python
#!/usr/bin/env python3
from user_pb2 import User

user = User(id=1, age=12, name='john')
print(user)

# write
with open('data.pb', 'wb') as f:
    f.write(user.SerializeToString())

# read
with open('data.pb', 'rb') as f:
    new_user = User()
    new_user.ParseFromString(f.read())

print(new_user)
```
