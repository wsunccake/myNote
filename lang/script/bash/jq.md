# jq

## filter

### basic

```bash
linux:~ $ echo '{"user": "jq", "scripts": ["bash", "perl", "python"]}' | jq '.'
{
  "user": "jq",
  "scripts": [
    "bash",
    "perl",
    "python"
  ]
}

linux:~ $ echo '{"user": "jq", "scripts": ["bash", "perl", "python"]}' | jq '.scripts'
[
  "bash",
  "perl",
  "python"
]

linux:~ $ echo '{"user": "jq", "scripts": ["bash", "perl", "python"]}' | jq '.scripts[]'
"bash"
"perl"
"python"

linux:~ $ echo '[{"user": "js", "lang": "javascript"}, {"user": "py", "lang": "python3"}]' | jq -r '.[].user, .[].lang' | paste -d, - -
js,py
javascript,python3

linux:~ $ echo '[{"user": "js", "lang": "javascript"}, {"user": "py", "lang": "python3"}]' | jq -r '.[] | .user, .lang' | paste -d, - -
js,javascript
py,python3
```

### list

```bash
linux:~ $ echo '[1, 2, 3]' | jq '. | map(. + 1)'
[
  2,
  3,
  4
]

linux:~ $ echo '[1, 2, 3]' | jq '.[] | select(. > 1)'
2
3

linux:~ $ echo '[1, 2, 3]' | jq '. | map(select(. > 1))'
[
  2,
  3
]

linux:~ $ echo '["bash", "python", "js"]' | jq '. | map("hello " + .)'
[
  "hello bash",
  "hello python",
  "hello js"
]

linux:~ $ echo '["bash", "python", "js"]' | jq '. | map(select(. == "js"))'
[
  "js"
]

linux:~ $ echo '[1, 2, 3]' | jq '. | max'
3
```

### object

```bash
linux:~ $ echo '{"a": 1, "b": 2, "c": 3}' | jq '. | map(. + 1)'
[
  2,
  3,
  4
]

linux:~ $ echo '{"a": 1, "b": 2, "c": 3}' | jq '. | map_values( .+ 1)'
{
  "a": 2,
  "b": 3,
  "c": 4
}

linux:~ $ echo '{"a": 1, "b": 2, "c": 3}' | jq '. | map(select(. > 1))'
[
  2,
  3
]

linux:~ $ echo '{"a": 1, "b": 2, "c": 3}' | jq '. | map_values(select(. > 1))'
{
  "b": 2,
  "c": 3
}
```

### mix

```bash
linux:~ $ echo '[{"lang": "bash"}, {"lang": "python"}, {"lang": "js"}]' | jq '. | map(.lang == "js")'
[
  false,
  false,
  true
]

linux:~ $ echo '[{"lang": "bash"}, {"lang": "python"}, {"lang": "js"}]' | jq '. | map(select(.lang == "js"))'
[
  {
    "lang": "js"
  }
]

linux:~ $ echo '[{"lang": "bash"}, {"lang": "python"}, {"lang": "js"}]' | jq '. | map_values(select(. == "js"))'
[
  {
    "lang": "python"
  }
]

linux:~ $ echo '[{"lang": "bash"}, {"lang": "python"}, {"lang": "js"}]' | jq '.[] | select(.lang == "js")'
{
  "lang": "js"
}

linux:~ $ echo '[{"lang": "bash"}, {"lang": "python"}, {"lang": "js"}]' | jq '.[] | map_values(select(. == "js"))'
{}
{}
{
  "lang": "js"
}

linux:~ $ echo '[{"like": 4, "lang": "bash"}, {"like": 9,"lang": "python"}, {"like": 8, "lang": "js"}]' | jq '. | max_by(.like)'
{
  "like": 9,
  "lang": "python"
}

linux:~ $ echo '[{"lang": "bash"},
  {"lang": "python", "books": ["learn python", "python book"]},
  {"lang": "js", "books": ["learn js"]}]' | \
  jq '.[].books'

[
  "learn python",
  "python book"
]
[
  "learn js"
]

linux:~ $ echo '[{"lang": "bash"},
  {"lang": "python", "books": ["learn python", "python book"]},
  {"lang": "js", "books": ["learn js"]}]' | \
  jq '.[].books' | cat
null
[
  "learn python",
  "python book"
]
[
  "learn js"
]

linux:~ $ echo '[{"lang": "bash"},
  {"lang": "python", "books": ["learn python", "python book"]},
  {"lang": "js", "books": ["learn js"]}]' | \
  jq '.[].books | .[]?'
"learn python"
"python book"
"learn js"

linux:~ $  echo '[{"lang": "bash"},
  {"lang": "python", "books": ["learn python", "python book"]},
  {"lang": "js", "books": ["learn js"]}]' | \
  jq '.'
[
  {
    "lang": "bash"
  },
  {
    "lang": "python",
    "books": [
      "learn python",
      "python book"
    ]
  },
  {
    "lang": "js",
    "books": [
      "learn js"
    ]
  }
]

linux:~ $ echo '[{"lang": "bash"},
  {"lang": "python", "books": ["learn python", "python book"]},
  {"lang": "js", "books": ["learn js"]}]' | \
  jq '.[]'
{
  "lang": "bash"
}
{
  "lang": "python",
  "books": [
    "learn python",
    "python book"
  ]
}
{
  "lang": "js",
  "books": [
    "learn js"
  ]
}

linux:~ $ echo '[{"lang": "bash"},
  {"lang": "python", "books": ["learn python", "python book"]},
  {"lang": "js", "books": ["learn js"]}]' | \
  jq '.[] | select(.lang | test("h"))'
{
  "lang": "bash"
}
{
  "lang": "python",
  "books": [
    "learn python",
    "python book"
  ]
}

linux:~ $ echo '[{"lang": "bash"},
  {"lang": "python", "books": ["learn python", "python book"]},
  {"lang": "js", "books": ["learn js"]}]' | \
  jq '.[] | select(.lang | test("h")) | .lang'
"bash"
"python"
```

---

## edit

### object

```bash
# add / +
linux:~ $ echo '{"user": "jq"}' | jq '. + {"msg": "hello jq"}'
{
  "user": "jq",
  "msg": "hello jq"
}

linux:~ $ echo '{}' | jq '. + {"msg": "hello jq"}'
{
  "msg": "hello jq"
}

# assign / =
linux:~ $ echo '{"user": "jq"}' | jq '. = {"msg": "hello jq"}'
{
  "msg": "hello jq"
}

linux:~ $ echo '{}' | jq '. = {"msg": "hello jq"}'
{
  "msg": "hello jq"
}

# del
linux:~ $ echo '{"user": "jq", "msg": "hello jq"}' | jq 'del(.msg)'
{
  "user": "jq"
}

linux:~ $ echo '{"user": "jq"}' | jq 'del(.msg)'
{
  "user": "jq"
}
```

### list

```bash
# add / +
linux:~ $ echo '[]' | jq '. + ["jq"]'
[
  "jq"
]

linux:~ $ echo '["hello"]' | jq '. + ["jq"]'
[
  "hello",
  "jq"
]

# assign / =
linux:~ $ echo '[]' | jq '. = "jq"'
"jq"

linux:~ $ echo '["hello"]' | jq '. = ["jq"]'
[
  "jq"
]
```

### mix

```bash
linux:~ $ echo '[{"lang":"bash"}]' | jq '. + [{"lang": "jq"}]'
[
  {
    "lang": "bash"
  },
  {
    "lang": "jq"
  }
]

linux:~ $ echo '[{"lang":"bash"}]' | jq '. = [{"lang": "jq"}]'
[
  {
    "lang": "jq"
  }
]
```

### mix

```bash
linux:~ $ echo '{"arr":[1],  "obj": {"a": "A"}}'  | jq '.arr + [2,3]'
[
  1,
  2,
  3
]


linux:~ $ echo '{"arr":[1],  "obj": {"a": "A"}}'  | jq '. + {"z": "Z"}'
{
  "arr": [
    1
  ],
  "obj": {
    "a": "A"
  },
  "z": "Z"
}

linux:~ $ echo '{"arr":[1],  "obj": {"a": "A"}}'  | jq '.obj + {"z": "Z"}'
{
  "a": "A",
  "z": "Z"
}


linux:~ $ echo '{"arr":[1],  "obj": {"a": "A"}}'  | jq '.obj += {"z": "Z"}'
{
  "arr": [
    1
  ],
  "obj": {
    "a": "A",
    "z": "Z"
  }
}
```
