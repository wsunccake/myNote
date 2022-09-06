# jmeter


## web

[Download Apache JMeter](https://jmeter.apache.org/download_jmeter.cgi)


---

## install

```bash
linux:~ # https://dlcdn.apache.org//jmeter/binaries/apache-jmeter-5.5.tgz
linux:~ # tar zxf apache-jmeter-5.5.tgz
linux:~ # ls /usr/local/apache-jmeter-5.5
linux:~ # ln -s /usr/local/apache-jmeter-5.5/bin/jmeter /usr/local/bin/jmeter
```


---

## usage

```bash
# gui
linux:~ $ jmeter

# cli
linux:~ $ export HEAP="-Xms1g -Xmx1g -XX:MaxMetaspaceSize=256m"
linux:~ $ jmeter -n -t <jmx file> \
  [-l <results file> -e -o <path to web report folder>]
```


---

## test

```
Test Plan
+-- Thread Group                    Threads (Users)
    +-- User Defined Variables      Config Element
    +-- CSV Data Set Config         Config Element
    +-- HTTP Request Defaults       Config Element
    +-- HTTP Header Manager         Config Element
    +-- HTTP Cookie Manager         Config Element
    +-- HTTP Request                Sampler
        +-- View Results Tree       Listener
        +-- View Results in Table   Listener
        +-- Summary Report          Listener
    +-- HTTP Request
        +-- JSR223 PreProcessor     Pre Processors
        +-- JSON Extractor          Listener
        +-- JSR223 PostProcessor    Post Processors
    +-- While Controller            Logical Controller
        +-- HTTP Request
            +-- JSR223 PreProcessor
            +-- JSR223 PostProcessor
    +-- OS Prcoess Sampler          Sampler
        +-- View Results Tree
    ...
```


---

## Config Element

### CSV Data Set Config

```
Filename:                               user.csv

Variable Names (comma-delimited):       USERNAME,PASSWORD
```


---

## Logical Controller

## While Controller

```
Condition (function or variable)        ${__groovy(
	!(vars.get("STATUS").equals("SUCCESS")) && (${RETRY}.toInteger() < ${LIMIT}.toInteger())
)}
```


---

## Sampler

### HTTP Request

```
Protocol [http]:                        http
Server Name or IP:                      www.google.com
```


### OS Prcoess Sampler

```
Command:                                ls
Working directory:
Command parameters:
```


---

## PreProcessor / PostProcessor

### JSR223 PreProcessor / PostProcessor

```groovy
import groovy.json.JsonOutput
import groovy.json.JsonSlurper

def jsonSlurper = new JsonSlurper()
def response = jsonSlurper.parseText(prev.getResponseDataAsString())
log.info(response.name)

def json = JsonOutput.toJson(response)
log.info(json)

// set variable
vars.put("data", json)

// get variable
def name = vars.get("name")
log.info(name)
```


### JSON Extractor

```
Names of created variables:             name; url
JSON Path expressions:                  $.name; $.url

Default Values:                         name; url
```


---

## ref

[壓測工具：JMeter 使用教學 + 自定義變數使用
](https://yuanchieh.page/posts/2021/2021-06-26-jmeter-%E4%BD%BF%E7%94%A8%E6%95%99%E5%AD%B8-+-%E8%87%AA%E5%AE%9A%E7%BE%A9%E8%AE%8A%E6%95%B8%E4%BD%BF%E7%94%A8/)

[Jmeter JSON Extractor 快速解析 API 的 Response](https://bingdoal.github.io/others/2020/12/jmeter-json-extractor/)
