# allure-pytest

## install

```bash
linux:~ # pip install allure-pytest
```


---

## usage

```bash
linux:~ # pytest --alluredir=./result
```


---

## install allure

```bash
linux:~ # wget https://repo1.maven.org/maven2/io/qameta/allure/allure-commandline/2.13.6/allure-commandline-2.13.6.zip
linux:~ # unzip allure-commandline-2.13.6.zip /usr/local
linux:~ # ln -s /usr/local/allure-2.13.6/bin/allure /usr/local/bin/.
```


---

## generate report

```bash
linux:~ # allure serve ./resutl

linux:~ # allure generate ./result -o ./report
linux:~ # allure open -h 127.0.0.1 -p 8080 ./report/
```
