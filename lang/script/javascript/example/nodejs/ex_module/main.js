var x1 = require('./my_module');
x1.setName('X1');
x1.sayHello();

var x2 = require('./my_module');
x2.setName('X2');
x2.sayHello();

x1.sayHello();


Hello1 = require('./Hello1').Hello1

var y1 = new Hello1();
y1.setName('Y1');
y1.sayHello();

var y2 = new Hello1();
y2.setName('Y2')
y2.sayHello();

y1.sayHello();


Hello2 = require('./Hello2');

var z1 = new Hello2();
z1.setName('Z1');
z1.sayHello();

var z2 = new Hello2();
z2.setName('Z2');
z2.sayHello();

z1.sayHello();