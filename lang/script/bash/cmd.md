# common command

## curl

### with ftp

```bash
# login
linux:~ # curl -v -u <username>:<password> "ftp://<ftp ip>/<path>/"

# upload
linux:~ # curl -v -u <username>:<password> "ftp://<ftp ip>/<path>/" -T "<file>" --ftp-create-dirs

# download
linux:~ # curl -v -u <username>:<password> "ftp://<ftp ip>/<path>/<file>" -o "<file>"

# rename
linux:~ # curl -v -u <username>:<password> "ftp://<ftp ip>/<path>" -Q "-RNFR <old file>"  -Q "-RNTO <new file>"

# remove
linux:~ # curl -v -u <username>:<password> "ftp://<ftp ip>/<path>" -Q "-DELE <file>"

# mkdir
linux:~ # curl -v -u <username>:<password> "ftp://<ftp ip>/<path>/" --ftp-create-dirs
linux:~ # curl -v -u <username>:<password> "ftp://<ftp ip>/" -Q "-MKD <path>"

# rmdir
linux:~ # curl -v -u <username>:<password> "ftp://<ftp ip>/" -Q "-RMD <path>"
```

---

## jq

```bash
linux:~ # echo '{"user": "jq", "scripts": ["bash", "perl", "python"]}' | jq '.'
linux:~ # echo '{"user": "jq", "scripts": ["bash", "perl", "python"]}' | jq '.scripts'
linux:~ # echo '{"user": "jq", "scripts": ["bash", "perl", "python"]}' | jq '.scripts[]'
linux:~ # echo '{"user": "jq"}' | jq '. + {"msg": "hello jq"}         # add/write
linux:~ # echo '{"user": "jq", "msg": "hello jq"}' | jq 'del(.msg)'   # del

linux:~ # echo '[{"user": "js", "lang": "javascript"}, {"user": "py", "lang": "python3"}]' | jq -r '.[].user, .[].lang' | paste -d, - -
linux:~ # echo '[{"user": "js", "lang": "javascript"}, {"user": "py", "lang": "python3"}]' | jq -r '.[] | .user, .lang' | paste -d, - -

# list 
linux:~ # echo '[1, 2, 3]' | jq '. | map(. + 1)'
linux:~ # echo '[1, 2, 3]' | jq '.[] | select(. > 1)'
linux:~ # echo '[1, 2, 3]' | jq '. | map(select(. > 1))'
linux:~ # echo '["bash", "python", "js"]' | jq '. | map("hello " + .)
linux:~ # echo '["bash", "python", "js"]' | jq '. | map(select(. == "js"))'
linux:~ # echo '[1, 2, 3]' | jq '. | max'

# object
linux:~ # echo '{"a": 1, "b": 2, "c": 3}' | jq '. | map(. + 1)'
linux:~ # echo '{"a": 1, "b": 2, "c": 3}' | jq '. | map_values( .+ 1)'
linux:~ # echo '{"a": 1, "b": 2, "c": 3}' | jq '. | map(select(. > 1))'
linux:~ # echo '{"a": 1, "b": 2, "c": 3}' | jq '. | map_values(select(. > 1))'

# mix
linux:~ # echo '[{"lang": "bash"}, {"lang": "python"}, {"lang": "js"}]' | jq '. | map(.lang == "js")'
linux:~ # echo '[{"lang": "bash"}, {"lang": "python"}, {"lang": "js"}]' | jq '. | map(select(.lang == "js"))'
linux:~ # echo '[{"lang": "bash"}, {"lang": "python"}, {"lang": "js"}]' | jq '. | map_values(select(. == "js"))'
linux:~ # echo '[{"lang": "bash"}, {"lang": "python"}, {"lang": "js"}]' | jq '.[] | select(.lang == "js")'
linux:~ # echo '[{"lang": "bash"}, {"lang": "python"}, {"lang": "js"}]' | jq '.[] | map_values(select(. == "js"))'
linux:~ # echo '[{"like": 4, "lang": "bash"}, {"like": 9,"lang": "python"}, {"like": 8, "lang": "js"}]' | jq '. | max_by(.like)'

linux:~ # echo '[{"lang": "bash"}, {"lang": "python", "books": ["learn python", "python book"]}, {"lang": "js", "books": ["learn js"]}]' | jq '.[].books' | cat
linux:~ # echo '[{"lang": "bash"}, {"lang": "python", "books": ["learn python", "python book"]}, {"lang": "js", "books": ["learn js"]}]' | jq '.[].books | .[]'
```

---

## content

```bash
linux:~ # csplit /etc/passwd 10
linux:~ # csplit /etc/passwd 10 {2}
linux:~ # csplit /etc/passwd 10 // '{*}'

linux:~ # sort /etc/passwd
linux:~ # sort -r /etc/passwd
linux:~ # sort -t: -k3 -n /etc/passwd

linux:~ # shuf /etc/passwd

linux:~ # uniq
```
