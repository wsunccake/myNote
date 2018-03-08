var http = require('http');
var querystring = require('querystring');
var req = http.request({host: 'localhost',
                        port: 3000,
                        path: '/',
                        method: 'POST',
});
var postData = querystring.stringify({
  'name': 'abc',
  'age': 12,
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


req.write(postData);
req.end();