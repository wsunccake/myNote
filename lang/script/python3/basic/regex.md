# regex

---

## content

- [match](#match)
- [search](#search)

---

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


# same as sh ${STR#*/}
restr = re.compile('(.*?)/(.*)').match(str)
print("%s <=> %s" %(restr.group(1), restr.group(2)))
print(re.sub('^(.*?)/', '', str))


# same as sh ${STR##*/}
restr = re.compile('(.*)/(.*)').match(str)
print("%s <=> %s" %(restr.group(1), restr.group(2)))
print(re.sub('(.*)/', '', str))
```

---

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
