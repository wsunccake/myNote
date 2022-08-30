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
