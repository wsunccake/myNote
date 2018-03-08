var http = require('http');
var util = require('util');
var url = require('url');
var querystring = require('querystring');

var server = new http.Server();

var myParser = function (str) {
  var re_parser = {};
  if (typeof (str) === 'string') {
    var strs = str.split('&');
    var re = /(.*)=(.*)/;
    for (var i in strs) {
      if (strs[i].match(re)) {
        var m = re.exec(strs[i]);
        re_parser[m[1]] = m[2];
      }
    }
  };
  return re_parser;
}

server.on('request', function (req, res) {
  res.writeHead(200, {'Content-Type': 'text/html'});

  // console.log(util.inspect(url.parse(req.url, true)));
  // console.log(util.inspect(req.url, true));
  // console.log(url.parse(req.url));
  // console.log(req);
  console.log('http methpd: %s', req.method);
  console.log(url.parse(req.url).query);
  var post = '';

  req.on('data', function (chunk) {
    post += chunk;
    var tmp = myParser(post);
    console.log('begin data event:');
    console.log(tmp);
    console.log('finish data event:');
    res.write('Hi ' + tmp.name);
    res.write('<br>Your ' + tmp.age + ' years old.');
    res.end();
  });

  req.on('end', function () {
    post = querystring.parse(post);
    console.log('begin end event:');
    console.log(post);
    console.log('finish end event:');
    res.end();
  });
});

server.listen(3000);
console.log("HTTP server is listening at port 3000.");