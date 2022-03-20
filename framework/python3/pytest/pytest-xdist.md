# pytest-xdist

## install

```bash
linux:~ # pip install pytest-bdd
```


---

## usage

```bash
# number of process
linux:~ $ pytest -n <N> <test file>.py

# subprocess
linux:~ $ pytest --dist=each --tx 3*popen//python=python3.6

# forked subprocess
linux:~ $ pytest --dist=each --tx 3*popen//python=python3.6 --boxed

# ssh slave
linux:~ $ pytest --dist=each --tx ssh=<user1>@<server1>//python="python" --tx ssh=ssh=<user2>@<server2>//python="python" --rsyncdir package package

# socket server
linux:~ $ wget https://raw.githubusercontent.com/pytest-dev/execnet/master/execnet/script/socketserver.py
linux:~ $ python socketserver.py :8889 &
linux:~ $ python socketserver.py :8890 &
linux:~ $ pytest --dist=each --tx socket=localhost:8889 --tx socket=localhost:8890

```


---

## ref

[pytest-xdist](https://pytest-xdist.readthedocs.io/en/latest/)
