var http = require('http');
var util = require('util');
var url = require('url');

var server = new http.Server();

server.on('request', function (req, res) {
  res.writeHead(200, {'Content-Type': 'text/html'});

  // console.log(util.inspect(url.parse(req.url, true)));
  // console.log(util.inspect(req.url, true));
  // console.log(url.parse(req.url));
  // console.log(req);
  console.log('http methpd: %s', req.method);
  var tmp_str = url.parse(req.url).query;
  var name = '';
  var age = '';

  if (typeof (tmp_str) === 'string') {
    var strs = tmp_str.split('&');
    for (var i in strs) {
      // console.log('%s: %s', i, strs[i]);
      if (strs[i].match('name=')) {
        var name = strs[i].replace('name=', '');
      }
      if (strs[i].match('age=')) {
        var age = strs[i].replace('age=', '');
      }
    }
    console.log('name: %s, age: %s', name, age);
    res.write('Hi ' + name);
    res.write('<br>Your ' + age + ' years old.');
    res.end();
  }
});

server.listen(3000);
console.log("HTTP server is listening at port 3000.");