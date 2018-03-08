var util = require('util');
var Person = function () {
  this.name = 'abc';
  this.toString = function () {
    return this.name;
  };
};

var obj = new Person();

console.log(util.inspect(obj));
console.log(util.inspect(obj, true));