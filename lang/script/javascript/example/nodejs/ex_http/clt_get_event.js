var http = require('http');
var req = http.get({host: 'localhost',
                    port: 3000,
                    path: '/?name=abc&age=123',
});

req.on('response', function (res) {
  res.setEncoding('utf8');
  res.on('data', function (data) {
    console.log(data);
  });
});

req.on('error', function (e) {
  console.log('error: ' + e.message);
});

req.end();