# run

## command

```bash
linux:~ $ python3 -c "print('Hello, Python')"
```


---

## interactive mode

```bash
linux:~ $ python3
```


---

## script

```python
#!/usr/bin/env python3

print('Hello, Python')
```

```bash
linux:~ $ chmod u+x hello.py
linux:~ $ ./hello.py
```

```bash
linux:~ $ python3 hello.py
```


---

## environmental variable

| variable 			| description 												|
| --- 				| --- 														|
| PYTHONPATH 		| module path, 預設為 /usr/lib/python<version>/site-packages 	|
| PYTHONHOME 		| 模組搜尋路徑相關的變數, 預設為 /usr/lib/python<version> 		|
| PYTHONSTARTUP 	| interactive mode 所執行程式路徑 								|
