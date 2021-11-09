# command

## common

```bash
linux:~ $ go help env
linux:~ $ go env GOPATH
linux:~ $ go env -w GO111MODULE=auto    # set go env
linux:~ $ cat $(go env GOENV)           # show go env
linux:~ $ go env -u GO111MODULE         # unset go env

linux:~ $ go build <go file>            # build
linux:~ $ go build ./...                # check all import, '...' wildcards

linux:~ $ go install
linux:~ $ go get
linux:~ $ go test
```


---

## env

```bash
linux:~ $ go help environment
linux:~ $ go env
linux:~ $ go env GOPATH
linux:~ $ go env -w GO111MODULE=auto    # set go env

GOROOT: root dir
GOPATH: workspace
GO111MODULE: module mode off, on, auto
GOBIN:
```


---

## module

```bash
linux:~/gomp $ go get github.com/fatih/color            # download module / package
linux:~/gomp $ go get github.com/fatih/color@v1.8.0
```
