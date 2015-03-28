// function Hello1() {
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