var http = require('http');
var option = {host: 'localhost',
              port: 3000,
              path: '/?name=abc&age=123'
};

http.get(option, function(res) {
  res.setEncoding('utf8');
  res.on('data', function (data) {
    console.log(data);
  });
});