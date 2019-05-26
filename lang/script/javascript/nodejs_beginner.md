# Node Beginner

## Create Project

```bash
linux:~ # mkdir project
linux:~ # cd project
linux:~/project # npm init
...
```

`package.json`

```json
{
  "name": "project",
  "version": "1.0.0",
  "main": "index.js",
  "scripts": {
    "start": "node index.js",
  },
  "author": "",
  "license": "ISC",
  "description": ""
}
```

scripts.start -> npm start

`index.js`

```javascript
var http = require("http");

http.createServer(function(request, response) {
  response.writeHead(200, {"Content-Type": "text/plain"});
  response.write("Hello World");
  response.end();
}).listen(8888);
```

http.createServer -> lanch service

http.createServer.listen -> setup port

request ->

response ->

`usage`

```bash
# run
linux:~/project # npm start

# test
linux:~ # curl localhost:8888
```


---

## Function

`index.js`

```javascript
var http = require("http");

function onRequest(request, response) {
  response.writeHead(200, {"Content-Type": "text/plain"});
  response.write("Hello World");
  response.end();
}

http.createServer(onRequest).listen(8888);
```

用 function (onRequest) 當 argument 帶入 http.createServer


---

## Module

`server.js`

```javascript
var http = require("http");

function start() {
    function onRequest(request, response) {
        response.writeHead(200, {"Content-Type": "text/plain"});
        response.write("Hello World");
        response.end();
    }

    http.createServer(onRequest).listen(8888);
}

exports.start = start;
```

`index.js`

```javascript
var server = require("./server");

server.start();
```


---

## Router

`requestHandlers.js`

```javascript
function start() { return "Hello Start"; }
function upload() { return "Hello Upload"; }

exports.start = start;
exports.upload = upload;
```

`router.js`

```javascript
function route(handle, pathname) {
    if (typeof handle[pathname] === 'function') {
        return handle[pathname]();
    } else {
        return "404 Not found";
    }
}

exports.route = route;
```

typeof ->

handle\[pathname]() ->

`server.js`

```javascript
let http = require("http");
let url = require("url");

function start(route, handle) {
    function onRequest(request, response) {
        let pathname = url.parse(request.url).pathname;
        let query = url.parse(request.url).query;
        console.log(pathname, query, request.method);

        if (pathname === '/favicon.ico') { return }
        let content = route(handle, pathname);

        response.writeHead(200, {"Content-Type": "text/plain"});
        response.write(content);
        response.end();
    }

    http.createServer(onRequest).listen(8888);
}

exports.start = start;
```
request.method -> http method: GET, POST, ...

request.url -> /xxx?var=abc

url.parse(request.url).pathname -> /xxx

url.parse(request.url).query -> var=abc

`index.js`

```javascript
let server = require("./server");
let router = require("./router");
let requestHandlers = require("./requestHandlers");

let handle = {};
handle["/"] = requestHandlers.start;
handle["/start"] = requestHandlers.start;
handle["/upload"] = requestHandlers.upload;

server.start(router.route, handle);
```

`usage`

```bash
# test
linux:~ # curl localhost:8888
linux:~ # curl localhost:8888/start
linux:~ # curl localhost:8888/upload
linux:~ # curl localhost:8888/stop
```


---

## Blocking

`requestHandlers.js`

```javascript
function start() {
    function sleep(milliSeconds) {
        let startTime = new Date().getTime();
        while (new Date().getTime() < startTime + milliSeconds) {}
    }

    // blocking function
    sleep(5000);
    return "Hello Start";
}

function upload() { return "Hello Upload"; }

exports.start = start;
exports.upload = upload;
```

`router.js`

```javascript
function route(handle, pathname) {
    if (typeof handle[pathname] === 'function') {
        return handle[pathname]();
    } else {
        return "404 Not found";
    }
}
```

`server.js`

```javascript
let http = require("http");
let url = require("url");

function start(route, handle) {
    function onRequest(request, response) {
        let pathname = url.parse(request.url).pathname;
        let query = url.parse(request.url).query;
        console.log(pathname, query, request.method);

        if (pathname === '/favicon.ico') { return }
        let content = route(handle, pathname);

        response.writeHead(200, {"Content-Type": "text/plain"});
        response.write(content);
        response.end();
    }

    http.createServer(onRequest).listen(8888);
}
```

`index.js`

```javascript
let server = require("./server");
let router = require("./router");
let requestHandlers = require("./requestHandlers");

let handle = {};
handle["/"] = requestHandlers.start;
handle["/start"] = requestHandlers.start;
handle["/upload"] = requestHandlers.upload;

server.start(router.route, handle);
```


---

## Non-Blocking

`requestHandlers.js`

```javascript
let exec = require("child_process").exec;

function start() {
    let content = "empty";
    let command = "find . -name \\*.js";

    // non-blocking function
    exec(command, function (error, stdout, stderr) {
        content = stdout;
        console.log(new Date().getTime(), 'in exec', content);
    });
    console.log(new Date().getTime(), 'out exec', content);
    return content;
}

function upload() { return "Hello Upload"; }

exports.start = start;
exports.upload = upload;
```

`router.js`

```javascript
function route(handle, pathname) {
    if (typeof handle[pathname] === 'function') {
        return handle[pathname]();
    } else {
        return "404 Not found";
    }
}
```

`server.js`

```javascript
let http = require("http");
let url = require("url");

function start(route, handle) {
    function onRequest(request, response) {
        let pathname = url.parse(request.url).pathname;
        let query = url.parse(request.url).query;
        console.log(pathname, query, request.method);

        if (pathname === '/favicon.ico') { return }
        let content = route(handle, pathname);

        response.writeHead(200, {"Content-Type": "text/plain"});
        response.write(content);
        response.end();
    }

    http.createServer(onRequest).listen(8888);
}
```

`index.js`

```javascript
let server = require("./server");
let router = require("./router");
let requestHandlers = require("./requestHandlers");

let handle = {};
handle["/"] = requestHandlers.start;
handle["/start"] = requestHandlers.start;
handle["/upload"] = requestHandlers.upload;

server.start(router.route, handle);
```

---

## Non-Blocking Response

`requestHandlers.js`

```javascript
let exec = require("child_process").exec;

function start(response) {
    let content = "empty";
    let command = "find . -name \\*.js";
    exec(command, function (error, stdout, stderr) {
        content = stdout;
        response.writeHead(200, {"Content-Type": "text/plain"});
        response.write(content);
        response.end();
    });
}

function upload(response) {
    response.writeHead(200, {"Content-Type": "text/plain"});
    response.write("Hello Upload");
    response.end();
}

function error404(response) {
    response.writeHead(404, {"Content-Type": "text/plain"});
    response.write("404 Not found");
    response.end();
}

exports.start = start;
exports.upload = upload;
exports.error404 = error404;
```

`router.js`

```javascript
function route(handle, pathname, response) {
    if (typeof handle[pathname] === 'function') {
        return handle[pathname](response);
    } else {
        return handle["/error404"](response);
    }
}

exports.route = route;
```

`server.js`

```javascript
let http = require("http");
let url = require("url");

function start(route, handle) {
    function onRequest(request, response) {
        let pathname = url.parse(request.url).pathname;
        let query = url.parse(request.url).query;
        console.log(pathname, query, request.method);
        if (pathname === '/favicon.ico') { return }

        route(handle, pathname, response);
    }
    http.createServer(onRequest).listen(8888);
}

exports.start = start;
```

`index.js`

```javascript
let server = require("./server");
let router = require("./router");
let requestHandlers = require("./requestHandlers");

let handle = {};
handle["/"] = requestHandlers.start;
handle["/start"] = requestHandlers.start;
handle["/upload"] = requestHandlers.upload;
handle["/error404"] = requestHandlers.error404;

server.start(router.route, handle);
```


---

## Template

`public/404.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>404 Error</title>
</head>
<body>
<b>404 No found</b>
</body>
</html>
```

`index.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{title}}</title>
</head>
<body>
{{content}}
</body>
</html>
```

`requestHandlers.js`

```javascript
let exec = require("child_process").exec;
let fs = require("fs");

function start(response) {
    let content = "empty";
    let command = "find . -name \\*.js";

    fs.readFile('public/index.html', function (err, data) {
        exec(command, function (error, stdout, stderr) {
            content = stdout;
            let html = data.toString()
                .replace('{{title}}', 'Start')
                .replace('{{content}}', content);
            response.writeHead(200, {"Content-Type": "text/plain"});
            response.end(html);
        });
    });
}

function upload(response) {
    fs.readFile('public/index.html', function (err, data) {
        let html = data.toString()
            .replace('{{title}}', 'Upload')
            .replace('{{content}}', 'Hello Upload');
        response.writeHead(200, {"Content-Type": "text/plain"});
        response.end(html);
    });
}

function error404(response) {
    fs.readFile('public/404.html', function (err, data) {
        response.writeHead(404, {"Content-Type": "text/plain"});
        response.end(data);
    });
}

exports.start = start;
exports.upload = upload;
exports.error404 = error404;
```

`router.js`

```javascript
function route(handle, pathname, response) {
    if (typeof handle[pathname] === 'function') {
        return handle[pathname](response);
    } else {
        return handle["/error404"](response);
    }
}

exports.route = route;
```

`server.js`

```javascript
let http = require("http");
let url = require("url");

function start(route, handle) {
    function onRequest(request, response) {
        let pathname = url.parse(request.url).pathname;
        let query = url.parse(request.url).query;
        console.log(pathname, query, request.method);
        if (pathname === '/favicon.ico') { return }

        route(handle, pathname, response);
    }
    http.createServer(onRequest).listen(8888);
}

exports.start = start;
```

`index.js`

```javascript
let server = require("./server");
let router = require("./router");
let requestHandlers = require("./requestHandlers");

let handle = {};
handle["/"] = requestHandlers.start;
handle["/start"] = requestHandlers.start;
handle["/upload"] = requestHandlers.upload;
handle["/error404"] = requestHandlers.error404;

server.start(router.route, handle);
```


---

## Ref

[Node入門](https://www.nodebeginner.org/index-zh-tw.html)
