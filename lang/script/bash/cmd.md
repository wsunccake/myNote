# common command

## jq

```bash
linux:~ # echo '{"user": "jq", "scripts": ["bash", "perl", "python"]}' | jq '.'
linux:~ # echo '{"user": "jq", "scripts": ["bash", "perl", "python"]}' | jq '.scripts'
linux:~ # echo '{"user": "jq", "scripts": ["bash", "perl", "python"]}' | jq '.scripts[]'
linux:~ # echo '{"user": "jq"}' | jq '. + {"msg": "hello jq"}         # add/write
linux:~ # echo '{"user": "jq", "msg": "hello jq"}' | jq 'del(.msg)'   # del

# list 
linux:~ # echo '[1, 2, 3]' | jq '. | map(. + 1)'
linux:~ # echo '[1, 2, 3]' | jq '.[] | select(. > 1)'
linux:~ # echo '[1, 2, 3]' | jq '. | map(select(. > 1))'
linux:~ # echo '["bash", "python", "js"]' | jq '. | map("hello " + .)
linux:~ # echo '["bash", "python", "js"]' | jq '. | map(select(. == "js"))'

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
```
