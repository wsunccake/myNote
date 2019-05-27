# Socket.IO


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
  "description": "",
  "main": "app.js",
  "scripts": {
    "start": "node app.js",
  },
  "keywords": [],
  "author": "",
  "license": "ISC",
  "dependencies": {
    "socket.io": "^2.2.0"
  }
}
```

`app.js`

```javascript
var app = require('http').createServer(handler);
var io = require('socket.io')(app);
var fs = require('fs');

app.listen(8000);

function handler (req, res) {
    fs.readFile(__dirname + '/index.html',
        function (err, data) {
            if (err) {
                res.writeHead(500);
                return res.end('Error loading index.html');
            }

            res.writeHead(200);
            res.end(data);
        });
}

io.on('connection', function (socket) {
    socket.emit('news', { hello: 'world' });
    socket.on('my other event', function (data) {
        console.log(data);
    });
});
```

`index.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/2.2.0/socket.io.slim.js"></script>
    <script>
        var socket = io('http://localhost:8000');
        socket.on('news', function (data) {
            console.log(data);
            socket.emit('my other event', { my: 'data' });
        });
    </script>
</head>
<body>

</body>
</html>
```
