# Node.js

## Introduction

Node.js 是一個事件驅動 I/O 伺服端 JavaScript 環境, 基於Google的V8引擎. 目的是為了提供撰寫可擴充網路程式, 如 Web 服務. 第一個版本由 Ryan Dahl 於 2009年 釋出, 後來, Joyent 僱用了 Dahl, 並協助發展Node.js
其他程式語言的類似開發環境, 包含T wisted 於 Python, Perl Object Environment 於 Perl, libevent 於 C, 和 EventMachine 於 Ruby. 與一般 JavaScript 不同的地方, Node.js 並不是在 Web 瀏覽器上執行, 而是一種在伺服器上執行的 Javascript 伺服端 JavaScript. Node.js 實作了部份 CommonJS.

[Node.js](https://nodejs.org/)

[Node.js wiki](http://zh.wikipedia.org/wiki/Node.js)


---

## Basic

一般執行 nodejs 可分為三種方式, Command, REPL, Script. 各有各的方便之處.

Command 適合一次性執行;

REPL 適合 debug;

Script 適合程式開發.

使用到的環境變數 NODE\_PATH, NODE\_MODULE\_CONTEXTS 和 NODE\_DISABLE\_COLORS.

| variable                | description                        |
| ----------------------- | ---------------------------------- |
| NODE\_PATH              | 設定 node module 路徑, 多路徑用 ; 分隔 |
| NODE\_MODULE\_CONTEXTS  | 設定為 1 時, 將載入所有 global context |
| NODE\_DISABLE\_COLORS   | 設定為 1 時, REPL 則不顯示顏色         |


---

## Install

`package`

```bash
centos:~ # yum install nodejs
centos:~ # node -v
```

`docker`

```bash
centos:~ # docker pull node
centos:~ # cat package.json
{
  "name": "docker_web_app",
  "version": "1.0.0",
  "description": "Node.js on Docker",
  "author": "First Last <first.last@example.com>",
  "main": "server.js",
  "scripts": {
    "start": "node server.js"
  },
  "dependencies": {
    "express": "^4.16.1"
  }
}

centos:~ # cat server.js
'use strict';

const express = require('express');

// Constants
const PORT = 8080;
const HOST = '0.0.0.0';

// App
const app = express();
app.get('/', (req, res) => {
  res.send('Hello world\n');
});

app.listen(PORT, HOST);
console.log(`Running on http://${HOST}:${PORT}`);

centos:~ # cat Dockerfile 
FROM node

WORKDIR /usr/src/app
COPY package*.json ./
RUN npm install
COPY . .

EXPOSE 8080
CMD [ "npm", "start" ]

centos:~ # docker build -t node-app .
centos:~ # docker run -d -p 8080:8080 --name node node-app
centos:~ # curl http://127.0.0.1:8080
```


---

## Hello

`command`

```bash
centos:~ # node -e 'console.log("Hello, %s", "Nodejs");'

centos:~ # echo 'console.log("Hello NodeJS");' | node -i
```

`script`

```bash
centos:~ # cat hello.js
console.log("Hello NodeJS");

centos:~ # node hello.js
```

`interactive mode`

```bash
centos:~ # node
> console.log("hello, world");
> process.exit()
```


---


## Different with Browser

`addTwo.js`

```javascript
var base = 2;

function addTwo(input) {
    return parseInt(input) + base;
};

exports.addTwo = addTwo;
```


`test.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <script src="addTwo.js"></script>
    <script>
        var base = 10;
        var result = addTwo(2);
        console.log(result);
    </script>
</head>
<body>
    <p>result: <script>result;</script></p>  <!-- result overwrite base, value = 12 -->
</body>
</html>
```


`test.js`

```javascript
var addTwo = require('./addTwo').addTwo;
var base = 10;
var result = addTwo(2);
console.log(result);  // result not overwrite base, value = 4
```


## npm 

npm 是 node.js 的套件管理工具, 在使用時可分為 global mode 和 local mode 兩種模式. global mode 是系統安裝, 安裝移除時需要 root 權限, 使用 global mode 安裝套件時, 所有使用者都可使用套件; local mode 是使用者個別安裝, 使用 local mode 安裝套件時, 只有該使用者都可使用該套件. node.js 預設為 local mode.

|  dir \ mode  | global mode                  |  local mode          |
| -------------|------------------------------|----------------------|
| path         | /usr/local/bin               | ~/node\_modules/.bin |
| module       | /usr/local/lib/node\_modeules | ~/node\_modeule     |

使用方式

```bash
# help
centos:~ $ npm help         # 顯示說明文件
centos:~ $ npm help install # 顯示指令說明文件
centos:~ $ npm -l           # 顯示指令

# list
centos:~ $ npm list    # 顯示已安裝套件
centos:~ $ npm list -g # 顯示系統已安裝套件

# search
centos:~ $ npm search pkg # 搜尋套件

# install
centos:~ $ npm install              # 根據 package.json 安裝套件
centos:~ $ npm install pkg          # 從 repository 安裝套件
centos:~ $ npm install pkg -P       # 安裝套件同時將套件資訊寫入 package.json 的 dependencies
centos:~ $ npm install pkg -D       # 安裝套件同時將套件資訊寫入 package.json 的 devDependencies
centos:~ $ npm install pkg -O       # 安裝套件同時將套件資訊寫入 package.json 的 optionalDependencies
centos:~ $ npm install pkg -g       # 安裝套件到系統預設目錄
centos:~ $ npm install ./pkg.tar.gz # 直接安裝套件
centos:~ $ npm install git+https://git@github.com/abc/pkg.git # 從 github 安裝套件
centos:~ $ npm install git+ssh://git@github.com/abc/pkg.git
centos:~ $ npm install git://github.com/abc/pkg.git#v0.1      # 從 github 安裝套件並指定版本

# uninstall
centos:~ $ npm uninstall pkg

# upgrade
centos:~ $ npm upgrade pkg

# other
centos:~ $ npm info pkg # 顯示套件資訊
centos:~ $ npm veiw pkg # 同上

centos:~ $ npm link pkg # 將 local pkg link to global pkg

centos:~/package $ npm  # 建立可發佈 package

centos:~/package $ npm publish # 發佈 package
centos:~/package $ npm unpublish
```

在 somepackage 目錄下建立名稱為 index.js


```bash
centos:~/somepackage $ cat index.js
exports.hello = function() {
    console.log('Hello.');
};

# 建立 package.json 紀錄 package 資訊, 填空需輸入 none
centos:~/somepackage $ npm init 
...

centos:~/somepackage $ cat package.json
{
    "name": "somepackage",
    "version": "0.0.1",
    "description": "some pkg",
    "main": "index.js",
    "scripts": {
        "test": "none"
    },
    "repository": {
        "type": "git",
        "url": "none"
    },
    "keywords": [
        "test"
    ],
    "author": "abc",
    "license": "ISC"
}

 # 安裝該套件
centos:~ $ npm install somepackage
```

[NPM 套件管理工具](https://github.com/nodejs-tw/nodejs-little-book/blob/master/zh-tw/node_npm.rst)

[npm 基本指令](http://dreamerslab.com/blog/tw/npm-basic-commands/)


### Version Rule

```
<major>.<minor>.<patch>

^: update to patch and minor, ^0.13.0 => 0.13.1, 0.14.0

~: update to patch, ~0.13.0 => 0.13.1

>: accept any higher than

>=: accept any equal to or higher than

<=: accept any version equal or lower to

<: accept any lower to

=: accept equal to

-: accept range of, 2.1.0 - 2.6.2

||: combine sets. Example: < 2.1 || > 2.6
```

[npm semver calculator](https://semver.npmjs.com/)

---

## Module and Package (CommonJS)

[`my_module.js`](./example/nodejs/ex_module/my_module.js)

```javascript
var name;

exports.setName = function(thyName) {
  name = thyName;
};

exports.sayHello = function() {
  console.log('Hello ' + name);
};
```


[`Hello1.js`](./example/nodejs/ex_module/Hello1.js)

```javascript
var Hello1 = function() {
	var name;
	this.setName = function (thyName) {
  	name = thyName;
	};

  this.sayHello = function () {
    console.log('Hello ' + name);
  };
};

exports.Hello1 = Hello1;
```


[`Hello2.js`](./example/nodejs/ex_module/Hello2.js)

```javascript
	var Hello2 = function() {
	  var name;
	
	  this.setName = function(thyName) {
	    name = thyName;
	  };
	
	  this.sayHello = function() {
	    console.log('Hello ' + name);
	  };
	};
	
	module.exports = Hello2;
```


[`main.js`](./example/nodejs/ex_module/main.js)

```javascript
// 沒使用 new
var x1 = require('./my_module');
x1.setName('X1');
x1.sayHello();

var x2 = require('./my_module');
x2.setName('X2');
x2.sayHello();

x1.sayHello();

// 使用 new
Hello1 = require('./Hello1').Hello1
var y1 = new Hello1();
y1.setName('Y1');
y1.sayHello();

var y2 = new Hello1();
y2.setName('Y2')
y2.sayHello();

y1.sayHello();

// new
Hello2 = require('./Hello2');

var z1 = new Hello2();
z1.setName('Z1');
z1.sayHello();

var z2 = new Hello2();
z2.setName('Z2');
z2.sayHello();

z1.sayHello();
```

[node.js 基本教學](http://dreamerslab.com/blog/tw/node-js-basics/)


---

## debug

[ex_bug.js](./example/nodejs/ex_bug.js)

```javascript
var a = 1;
var b = 'world';
var c = function (x) {
  console.log('hello ' + x + a);
};

c(b);
```

在終端機下執行

```bash
centos:~ $ node debug ex_bug.js
< Debugger listening on port 5858
connecting to port 5858... ok
break in ex_bug.js:1
> 1 var a = 1;
  2 var b = 'world';
  3 var c = function (x) {
  4   console.log('hello ' + x + a);
  5 };
```

另一種遠端執行

```bash
centos:~ $ node --debug-brk ex_bug.js
centos:~ $ node debug 127.0.0.1:5858
```

---

## Common Module


### console

類似 C 的 printf 的格式化輸出, 測試執行時間

[`run_time.js`](./example/nodejs/ex_console/run_time.js)

```javascript
console.log(global);
console.log(__dirname);
console.log(__filename);

console.time('Run loop');
for (var i = 10; i--;) {
  console.log('%d loop', i);
}
console.timeEnd('Run loop');
```


### process

[`argv.js`](./example/nodejs/ex_process/argv.js)

參數使用方式

```javascript
console.log(process.cwd());
console.log(process.chdir('..'));
console.log(process.argv);
```

執行並輸入參數

```bash
centos:~ $ node argv.js 123 -v "xyz ABC"
```

[`keyin.js`](./example/nodejs/ex_process/keyin.js)

從 stdin 輸入後並輸出在 stdout

```javascript
process.stdin.resume();

process.stdin.on('data', function(data) {
  process.stdout.write('read from console: ' + data.toString());
});
```


### filesystem

`non-blocking I/O 讀檔`

[`readfile.js`](./example/nodejs/ex_fs/readfile.js)

```javascript
var fs = require('fs');

console.log('start.');
fs.readFile('file.txt', 'utf-8', function(err, data) {
  if (err) {
    console.error(err);
  }
  else {
    console.log(data);
  }
});
console.log('end.');
```


`blocking I/O 讀檔`

[`readfilesync.js`](./example/nodejs/ex_fs/readfilesync.js)

```javascript
var fs = require('fs');
console.log('start.');
var data = fs.readFileSync('file.txt', 'utf-8');
console.log(data);
console.log('end.');
```


`以 C 的方式讀檔案`

[`readc.js`](./example/nodejs/ex_fs/readc.js)

	var fs = require('fs');
	
	fs.open('file.txt', 'r', function(err, fd) {
	  if (err) {
	    console.error(err);
	    return;
	  }
	
	  var buf = new Buffer(8);
	
	  fs.read(fd, buf, 0, 8, null, function(err, bytesRead, buffer) {
	    if (err) {
	      console.error(err);
	      return;
	    }
	
	    console.log('bytesRead: ' + bytesRead);
	    console.log(buffer);
	  })
	});


### os

[`sysinfo.js`](./example/nodejs/ex_os/sysinfo.js)

```javascript
var os = require('os');

console.log(os.cpus() );
console.log(os.networkInterfaces() );
```

### utils


### Event

[`event1.js`](./example/nodejs/ex_event/event1.js)

```javascript
console.log('Start');

setTimeout(function() {
  console.log('Trigger');
}, 1000);

console.log('End');
```


[`event2.js`](./example/nodejs/ex_event/event2.js)

```javascript
console.log('Start');

setTimeout(function() {
  console.log('Trigger');
}, 0);

console.log('End');
```


[`event3.js`](./example/nodejs/ex_event/event3.js)

```javascript
var EventEmitter = require('events').EventEmitter;
var event = new EventEmitter();

event.on('some_event', function() {
  console.log('some_event occured.');
});

setTimeout(function() {
  event.emit('some_event');
}, 1000);
```


[`event4.js`](./example/nodejs/ex_event/event4.js)

```javascript
var events = require('events');
var emitter = new events.EventEmitter();

emitter.on('someEvent', function(arg1, arg2) {
  console.log('listener1', arg1, arg2);
});
emitter.on('someEvent', function(arg1, arg2) {
  console.log('listener2', arg1, arg2);
});

emitter.emit('someEvent', 'abc', 123);
```


### http

[`app1.js`](./example/nodejs/ex_http/app1.js)

```javascript
var http = require("http");

http.createServer(function(req, res) {
  res.writeHead(200, {'Content-Type': 'text/html'});
  res.write('<h1>Node.js</h1>');
  res.end('<p>Hello World</p>');
}).listen(3000);
console.log("HTTP server is listening at port 3000.");
```

執行

```bash
centos:~ $ node app.js # 使用 node 直接執行, 在瀏覽器上輸入 localhost:3000 可看到
```

每次改 code, 都需要重新執行 node, 建議安裝 [nodemon](http://nodemon.io/), [node-supervisor](https://github.com/isaacs/node-supervisor), [node-dev](https://github.com/fgnass/node-dev) 或 [forever](https://github.com/nodejitsu/forever) 這類型 automaticall restart 代替 node 去執行

```bash
centos:~ $ nodemon app.js # 使用 nodemon
centos:~ $ supervisor app.js # 使用 node-supervisor
centos:~ $ forever -w app.js # 使用 forever
centos:~ $ node-dev app.js
```


以 Event 的方式使用 http

[`app2.js`](./example/nodejs/ex_http/app2.js)

```javascript
var http = require('http');
var server = new http.Server(); server.on('request', function(req, res) {
  res.writeHead(200, {'Content-Type': 'text/html'});
  res.write('<h1>Node.js</h1>');
  res.end('<p>Hello World</p>');
});

server.listen(3000);
console.log("HTTP server is listening at port 3000.");
```

[nodejs beginner](./nodejs_beginner.md)

[gulp入門指南](https://987.tw/2014/07/09/gulpru-men-zhi-nan/)
