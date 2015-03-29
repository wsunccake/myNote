var util = require('util');

function Base() {
  this.name = 'base'; // private member
  this.base = 1991;
  this.sayHello = function () { // private method
    console.log('Hello ' + this.name);
  };
}
Base.prototype.showName = function() { // public method
  console.log(this.name);
};

function Sub() {
  this.name = 'sub'; // private member
}
util.inherits(Sub, Base); // Sub inherit Base

var objBase = new Base();
objBase.showName();
objBase.sayHello();
console.log(objBase);

var objSub = new Sub();
objSub.showName();
// objSub.sayHello(); // without this method (private method)
console.log(objSub);