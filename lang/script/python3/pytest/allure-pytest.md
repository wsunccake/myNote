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

## testcase

`tests.py`

```python
import allure


@allure.step('login')
def login():
    print('login')


@allure.step('create xxx')
def create_xxx():
    print('create xxx')


@allure.step('create yyy')
def create_yyy():
    print('create yyy')


@allure.step('check xxx')
def check_xxx():
    print('check xxx')


@allure.step('check yyy')
def check_yyy():
    print('check yyy')


@allure.step('delete xxx')
def delete_xxx():
    print('delete xxx')


@allure.feature('xxx')
@allure.story('create and delete xxx')
def test_create_xxx():
    login()
    create_xxx()
    check_xxx()


@allure.feature('xxx')
@allure.story('create and delete xxx')
@allure.title('delete xxx')
def test_delete_xxx():
    login()
    delete_xxx()


@allure.feature('yyy')
@allure.story('create yyy')
def test_yyy():
    login()
    create_yyy()
    check_yyy()
```


---

## generate report

```bash
linux:~ # pytest --alluredir=result --clean-alluredir

linux:~ # allure serve result

linux:~ # allure generate result --clean
linux:~ # allure open
```
