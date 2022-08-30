# format output

## old format

```python
print('%s' % 42)
print('%f' % 7.03)
print('%d%%' % 100)

print('this %s a %s test' % ('is', 'simple'))
```


---

## new format

```python
print('{},{},{}'.format('ecmadao', 'edward', 'cavalier'))
print('{2},{0},{1}'.format('ecmadao', 'edward', 'cavalier'))

example_dict = {'a': 0, 'b': 1, 'c': 2}
print('{a} {b} {c}'.format(a = 0, b = 1, c = 2))
print('{0[a]} {0[b]} {0[c]}{1}'.format(example_dict, 'others'))

print('{0: f}'.format(7.03))
```


---

## here document

```python
print('''hello python2
hi python3''')
```
