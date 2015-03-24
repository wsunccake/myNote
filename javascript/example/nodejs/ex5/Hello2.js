// function Hello2() {
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