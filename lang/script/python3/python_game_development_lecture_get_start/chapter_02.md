# chapter 02

## run

```bash
linux:~ $ cat << EOF > hello.py
print("Hello World")
EOF

linux:~ $ python3 hello.py
```


---

## lint

```bash
linux:~ $ pip install pylint
linux:~ $ pylint hello.py
```


---

## format comform

```bash
linux:~ $ pip install autopep8
linux:~ $ autopep8 hello.py
```


---

## vscode setting

```javascript
// settings.json
{
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    // "python.linting.pylintArgs": ["--disable=C0111"],
    "files.trimTrailingWhitespace": true,
    "[python]":{
        "editor.formatOnType": true,
        "editor.formatOnSave": true,
        "editor.insertSpaces": true,
        "editor.detectIndentation": true,
        "editor.tabSize": 4
    }
}
```
