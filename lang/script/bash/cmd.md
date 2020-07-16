# common command

## jq

```bash
linux:~ # echo '{"user": "jq", "scripts": ["bash", "perl", "python"]}' | jq '.'
linux:~ # echo '{"user": "jq", "scripts": ["bash", "perl", "python"]}' | jq '.scripts'
linux:~ # echo '{"user": "jq", "scripts": ["bash", "perl", "python"]}' | jq '.scripts[]'
linux:~ # echo '{"user": "jq"}' | jq '. + {"msg": "hello jq"}        # add/write
linux:~ # echo '{"user": "jq", "msg": "hello jq"}'| jq 'del(.msg)'   # del
```
