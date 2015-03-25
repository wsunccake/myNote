# Node.js #

Node.js 是一個事件驅動 I/O 伺服端 JavaScript 環境, 基於Google的V8引擎. 目的是為了提供撰寫可擴充網路程式, 如 Web 服務. 第一個版本由 Ryan Dahl 於 2009年 釋出, 後來, Joyent 僱用了 Dahl, 並協助發展Node.js
其他程式語言的類似開發環境, 包含T wisted 於 Python, Perl Object Environment 於 Perl, libevent 於 C, 和 EventMachine 於 Ruby. 與一般 JavaScript 不同的地方, Node.js 並不是在 Web 瀏覽器上執行, 而是一種在伺服器上執行的 Javascript 伺服端 JavaScript. Node.js 實作了部份 CommonJS.

[Node.js](https://nodejs.org/)

[Node.js wiki](http://zh.wikipedia.org/wiki/Node.js)


### 基本操作 ###

一般執行 nodejs 可分為三種方式, Command, REPL, Script. 各有各的方便之處. Command 適合一次性執行; REPL 適合 debug; Script 適合程式開發. 使用到的環境變數 NODE\_PATH, NODE\_MODULE\_CONTEXTS 和 NODE\_DISABLE\_COLORS.

| variable                | description                        |
| ----------------------- | ---------------------------------- |
| NODE\_PATH              | 設定 node module 路徑, 多路徑用 ; 分隔 |
| ----------------------- | ---------------------------------- |
| NODE\_MODULE\_CONTEXTS  | 設定為 1 時, 將載入所有 global context |
| ----------------------- | ---------------------------------- |
| NODE\_DISABLE\_COLORS   | 設定為 1 時, REPL 則不顯示顏色         |



#### Command ####

	linux:~ $ node -e 'console.log("Hello, %s", "Nodejs");'


#### REPL (Read–Eval–Print Loop) ####

	linux:~ $ node
	> console.log("Hello Node.js");


#### Script  ####

[`hi.js`](./example/nodejs/ex1/hi.js)

	console.log("Hello Node.js");

執行

	linux:~ $ node hi.js


-----------------------------

#### npm ####

npm 是 node.js 的套件管理工具, 在使用時可分為 global mode 和 local mode 兩種模式. global mode 是系統安裝, 安裝移除時需要 root 權限, 使用 global mode 安裝套件時, 所有使用者都可使用套件; local mode 是使用者個別安裝, 使用 local mode 安裝套件時, 只有該使用者都可使用該套件. node.js 預設為 local mode.

|  dir \ mode  | global mode                  |  local mode          |
| -------------------------------------------------------------------|
| path         | /usr/local/bin               | ~/node\_modules/.bin |
| module       | /usr/local/lib/node\_modeules | ~/node\_modeule     |

使用方式

	# list
	linux:~ $ npm list # 顯示已安裝套件
	linux:~ $ npm list -g # 顯示系統已安裝套件

	# search
	linux:~ $ npm search pkg # 搜尋套件

	# install
	linux:~ $ npm install pkg # 安裝套件
	linux:~ $ npm install -g pkg # 安裝套件

	linux:~ $ npm uninstall pkg
	
	linux:~ $ npm info pkg
	linux:~ $ npm link pkg
	linux:~ $ npm help
	linux:~ $ npm help install


-----------------------------

### Module and Package (CommonJS) ###

### 常用模組 ###


#### console ####

類似 C 的 printf 的格式化輸出, 測試執行時間

[`run_time.js`](./example/nodejs/ex_console/run_time.js)

	console.log(global);
	console.log(__dirname);
	console.log(__filename);
	
	console.time('Run loop');
	for (var i = 10; i > 0; i--) {
	  console.log('%d loop', i);
	}
	console.timeEnd('Run loop');


#### process ####

[`argv.js`](./example/nodejs/ex_process/argv.js)

參數使用方式

	console.log(process.argv);

執行並輸入參數

	linux:~ $ node argv.js 123 -v "xyz ABC"

[`keyin.js`](./example/nodejs/ex_process/keyin.js)

從 stdin 輸入後並輸出在 stdout

	process.stdin.resume();
	
	process.stdin.on('data', function(data) {
	  process.stdout.write('read from console: ' + data.toString());
	});


#### filesystem####

non-blocking I/O 讀檔

[`readfile.js`](./example/nodejs/ex3/readfile.js)

	var fs = require('fs');

	fs.readFile('file.txt', 'utf-8', function(err, data) {
	  if (err) {
	    console.error(err);
	  }
	  else {
	    console.log(data);
	  }
	});
	console.log('end.');

blocking I/O 讀檔

[`readfilesync.js`](./example/nodejs/ex3/readfilesync.js)

	var fs = require('fs');
	var data = fs.readFileSync('file.txt', 'utf-8');

	console.log(data);
	console.log('end.');

以 C 的方式讀檔案


#### os ####

#### utils ####

#### Event ####

[`event1.js`](./example/nodejs/ex4/event1.js)

	console.log('Start');
	
	setTimeout(function() {
	  console.log('Trigger');
	}, 1000);
	
	console.log('End');


[`event2.js`](./example/nodejs/ex4/event2.js)

	console.log('Start');
	
	setTimeout(function() {
	  console.log('Trigger');
	}, 0);
	
	console.log('End');


[`event3.js`](./example/nodejs/ex4/event3.js)

	var EventEmitter = require('events').EventEmitter;
	var event = new EventEmitter();
	
	event.on('some_event', function() {
	  console.log('some_event occured.');
	});
	
	setTimeout(function() {
	  event.emit('some_event');
	}, 1000);


#### http ####

[`app1.js`](./example/nodejs/ex_http/app1.js)

	var http = require("http");

	http.createServer(function(req, res) {
	  res.writeHead(200, {'Content-Type': 'text/html'});
	  res.write('<h1>Node.js</h1>');
	  res.end('<p>Hello World</p>');
	}).listen(3000);
	console.log("HTTP server is listening at port 3000.");

執行

	linux:~ $ node app.js # 使用 node 直接執行, 在瀏覽器上輸入 localhost:3000 可看到

每次改 code, 都需要重新執行 node, 建議安裝 [nodemon](http://nodemon.io/), [node-supervisor](https://github.com/isaacs/node-supervisor), [node-dev](https://github.com/fgnass/node-dev) 或 [forever](https://github.com/nodejitsu/forever) 這類型 automaticall restart 代替 node 去執行

	linux:~ $ nodemon app.js # 使用 nodemon
	linux:~ $ supervisor app.js # 使用 node-supervisor
	linux:~ $ forever -w app.js # 使用 forever
	linux:~ $ node-dev app.js

以 Event 的方式使用 http

[`app2.js`](./example/nodejs/ex_http/app2.js)

	var http = require('http');
	var server = new http.Server(); server.on('request', function(req, res) {
	  res.writeHead(200, {'Content-Type': 'text/html'});
	  res.write('<h1>Node.js</h1>');
	  res.end('<p>Hello World</p>');
	});
	
	server.listen(3000);
	console.log("HTTP server is listening at port 3000.");
[gulp入門指南](https://987.tw/2014/07/09/gulpru-men-zhi-nan/)