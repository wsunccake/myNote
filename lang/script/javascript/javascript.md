# Javascript


## Run

`browser`

```html
<!DOCTYPE html>
<html>
<head>
</head>

<body>
<script>
    console.log('Hello JavaScript');
</script>
</body>
</html>
```


`node.js`

```bash
# REPL
linux:~ # node
> console.log('Hello JavaScript');
> process.exit()

# command
linux:~ # node -e 'console.log("Hello, %s", "Nodejs");'
linux:~ # echo 'console.log("Hello NodeJS");' | node -i

# script
linux:~ # cat hello.js
console.log('Hello JavaScript');

linux:~ # node hello.js
```


`rhino`

```bash
# REPL
linux:~ # java -jar js.jar
js> console.log('Hello JavaScript');

# script
linux:~ # cat helle.js
console.log('Hello JavaScript');

linux:~ # java -jar js.jar hello.js
```


---

## Comment

```javascript
// 這是單行註解 
/* 這是跨行註解 */ 
```


---

## Variable

var 會有 hosting, let 和 const 只會存在 block scope


### var

```javascript
var var1 = 123;
var var2;

var v1 = 1;
console.log(v1);

// hosting
console.log(v2);
var v2 = 2;

// console.log(v3); 
```


### let

```javascript
for (let i in [1, 2, 3]) {
    console.log(i);
}

let l1 = 1;
console.log(l1);

// l2 在使用前必先宣告
// console.log(l2);
let l2 = 2;
```


### const

```javascript
const pi = 3.14;

const peopel = ["Mary", "Joe"];
people.push("Telsa");

var humans = people
humans = "evil";

const frozen = Object.freeze(["Ice", "Ice cube"]);
frozen.push("Water");
```


---

## Data Type

JavaScript 中的變數分為 numerical, string, boolean 和 object type 有 array, object, resource, NULL. 變數宣告要使用 var (沒宣告 var 也可以, 但變數會成為全域變數), 變數名稱的開頭必須是底線（_）或英文字母, 英文字母的大小寫都可以, 而且大小寫有別, 要注意數字不可以作為變數的開頭.


### String

```javascript
let single = 'single-quoted';
let double = "double-quoted";
let backticks = `backticks`;
let multiline = `John
Pete
Mary
`;

console.log('single ${single}');
console.log("double ${double}");
console.log(`backticks ${backticks}`);

// inline
function sum(a, b) {
  return a + b;
}
console.log(`1 + 2 = ${sum(1, 2)}.`);

// common method
'Interface'.length;
'Interface'.toUpperCase();
'Interface'.toLowerCase();

// search string
"JavaScript,PHP,Python,Ruby".indexOf("JavaScript");
"JavaScript,PHP,Python,Ruby".indexOf("js");
"JavaScript,PHP,Python,Ruby".includes("JavaScript");
"JavaScript,PHP,Python,Ruby".includes("js");

// slice
"JavaScript".slice(4);
"JavaScript".slice(0, 4);

// loop
for (let char of "Hello") {console.log(char);}                 // H e l l o
for (let char in "Hello") {console.log(char, "Hello"[char]);}  // 0 1 2 3 4
[..."Hello"].forEach(c => console.log(c));                     // H e l l o

// split to list
"JavaScript,PHP,Python,Ruby".split(" ");

// string to number
Number("123");
parseInt("123");
parseFloat("123.0");

// string add
"abc" + "xyz";
```


### Number

```javascript
let num1 = 1;          // 十進位
let num2 = 0xff;       // 十六進位
let num3 = 033;        // 八進位
let num4 = 1234.5678;  // 浮點數
let num5 = 6.02e23;    // 使用科學記號 6.02 x 10 23
	
num4.toFixed(0);
num4.toExponential(1);
num4.toPrecision(3);

// rounding
Math.floor(num4);
Math.ceil(num4);
Math.round(num4);
Math.trunc(num4);

Math.random();
Math.max(1, 2)
Math.min(1, 2);
	
// number to string
let str0 = num1 + "";       // 第一種方法
let str0 = String(num1);    // 第二種方法
let str0 = num1.toString;   // 第三種方法

// NaN
isNaN(NaN);
NaN == NaN;                 // false

// Infinity
isFinite(Infinity)
Infinity == Infinity;       // true
```


### Boolean

```javascript
// 0 or Nan is false, 1 is true
var bool1 = true;
var bool2 = false;

// 轉Boolean 
Boolean("true"); 
!!1;

// Opera 8.0+
var isOpera = (!!window.opr && !!opr.addons) || !!window.opera || navigator.userAgent.indexOf(' OPR/') >= 0;

// Firefox 1.0+
var isFirefox = typeof InstallTrigger !== 'undefined';

// Safari 3.0+ "[object HTMLElementConstructor]" 
var isSafari = /constructor/i.test(window.HTMLElement) || (function (p) { return p.toString() === "[object SafariRemoteNotification]"; })(!window['safari'] || (typeof safari !== 'undefined' && safari.pushNotification));

// Internet Explorer 6-11
var isIE = /*@cc_on!@*/false || !!document.documentMode;

// Edge 20+
var isEdge = !isIE && !!window.StyleMedia;

// Chrome 1+
var isChrome = !!window.chrome && !!window.chrome.webstore;

// Blink engine detection
var isBlink = (isChrome || isOpera) && !!window.CSS;
```


### Array

```javascript
var arr1 = [1, 2, 3];
var arr2 = new Array(1, 2, 3);
var fruits = ["Apple", "Orange", "Pear"];
var emptyArray1 = [];            // empty array
var emptyArray2 = new Array;     // empty array

[1, 2, 3].length;

fruits.pop();             // remove last element
fruits.push("Pear");      // append
fruits.shift();           // remove first element
fruits.unshift('Apple');  // add first elemnt

[2, 3, 1].sort();
[2, 3, 1].reverse();

["do", "re", "mi"].join(" ");   // array to string
"do,re,mi".split(',');          // string to array
["do", "re", "mi"].concat("fa", ["so", "ra"])

// loop
for (let i = 0; i < fruits.length; i++) {
    console.log(fruits[i]);
}

for (let key in fruits) {
    console.log(fruits[key]);
}

for (let fruit of fruits) {
    console.log(fruit);
}

// for each
["Bilbo", "Gandalf", "Nazgul"].forEach(function(item, index, array) {
    alert(`${item} is at index ${index} in ${array}`);
});

["Bilbo", "Gandalf", "Nazgul"].forEach(alert);

["Bilbo", "Gandalf", "Nazgul"].forEach((item, index, array) => {
    alert(`${item} is at index ${index} in ${array}`);
});

// map
var result = ["Bilbo", "Gandalf", "Nazgul"].map(function(item, index, array) {
    return item.length;
});

["Bilbo", "Gandalf", "Nazgul"].map(item => item.length)

// find
[1, 2, 3, 4].find(function(item, index, array) {
    if (item > 2) return true
});

[1, 2, 3, 4].find(item => item > 2);

// filter
var users = [
  {id: 1, name: "John"},
  {id: 2, name: "Pete"},
  {id: 3, name: "Mary"}
];

var someUsers = users.filter((function(item, index, array) {
	return item.id < 3
});

users.filter(item => item.id < 3);

//reduce
[1, 2, 3, 4, 5].reduce(function(previousValue, item, index, arr) {
	return previousValue + item
}, inital);

[1, 2, 3, 4, 5].reduce((sum, current) => sum + current, 0);
```


### Object

```javascript
// object literal 方式宣告
var user = {
  name: "John",
  age: 30
};
user["money"] = 500;
var emptyObject1 = {};              // empty object
var emptyObject2 = new Object();    // empty object

// exist
user.noSuchProperty === undefined;
"key" in object;

// loop
for(let key in user) {
    console.log(key + " => " + user[key]);
}

Object.keys(user).forEach(p => console.log(`${p}: ${user[p]}`));
```

```javascript
// 定義全域變數 
var MYGLOBAL = {} || MYGLOBAL;
MYGLOBAL.var1 = "xyz";
MYGLOBAL.var2 = 123;
```


### null

```javascript
let n = null;

console.log("null: ", n);
console.log(n == null);
console.log(n != null);
console.log(n === null);
console.log(n !== null);
```


### undefined

```javascript
let d;

console.log("undefined: ", d);
console.log(d == undefined);
console.log(d != undefined);
console.log(d === undefined);
console.log(d !== undefined);
```


### Symbol

```javascript
let s1 = Symbol('js');
let s2 = Symbol('js');

console.log("s1: ", s1, "s2 :", s2);
console.log(s1 == s2);
console.log(s1 != s2);
console.log(s1 === s2);
console.log(s1 !== s2);
```


### Set


### Map


### type conversion

```javascript
console.log(8 * null);             // 0
console.log("5" * 2);              // 10
console.log("five" * 2);           // Nan
console.log(false == 0);           // true
console.log(null == undefined);    // true
console.log(null == 0);            // false

console.log(false === 0);          // false
```

---

## Operator

```javascript
let x, y;
x = y = 15;

console.log("to do: ", x);
console.log("doing: ", x++);
console.log("done: ", x);

console.log("to do: ", y);
console.log("doing: ", ++y);
console.log("done: ", y);
```


### typeof

```javascript
console.log("undefined: ", typeof undefined);
console.log("null: ", typeof null);
console.log("object: ", typeof {});
console.log("number: ", typeof 1);
console.log("string: ", typeof "abc");
console.log("true: ", typeof true);
console.log("symbol: ", typeof Symbol());
console.log("function", typeof function() {});
```


### compare

```javascript
const x = 5;
const y = "5";

console.log("==: ", x == y);
console.log("===: ", x === y);
console.log("!=: ", x != y);
console.log("!==: ", x !== y);
```


### destructuring assignment

`array destructure`

```javascript
let [firstname = "John", , ,lastname = "Doe"] = ["James", "L.", "Howlett"];
console.log(firstname, lastname);

let right = 1;
let left = 2;
console.log(right, left);
[right, left] = [left, right];
console.log(right, left);

[a, b, ...other] = [1, 2, 3, 4, 5];
console.log(a, b, other);
```


`object destructure`

```javascript
let {name: n, age: a=10} = {name: 'Jane'};
console.log(n, a);

let {name, age} = {name: 'Jane'};
console.log(name, age);
```

---

## Condition


### if/else

```
window.location
<protocol>//<hostname>:<port>/<pathname><search><hash>

href - the entire URL
protocol - the protocol of the URL
host - the hostname and port of the URL
hostname - the hostname of the URL
port - the port number the server uses for the URL
pathname - the path name of the URL
search - the query portion of the URL
hash - the anchor portion of the URL
```

```html
<html>
<body>
<script>
    var parameter = window.location.search;
    parameter = parameter.slice(1, parameter.length);
    var sex = parameter.split("=")[1];
    if (sex == "m") {
        console.log("Male");
    } else if (sex == "f") {
        console.log("Female");
    } else {
        console.log("Unknown");
    }
</script>
</body>
</html>
```

```bash
# commoand
linux:~ # curl http://127.0.0.1/ex.html?sex=m
```

```javascript
var browser;
if (!!window.chrome) {
    browser = "Chrome";
} else {
    browser = "Unknown";
}
console.log(browser);

//  使用 ?: ternary operator
browser = (!!window.chrome) ? "Chrome" : "Unknown";
console.log(browser);
```

```javascript
if (!options) {
    options = {}
}

//  使用 || 簡化空值判斷
options = options || {};
```


### switch

```javascript
// 同 if/else, 改用 switch 方式
var parameter = window.location.search;
parameter = parameter.slice(1, parameter.length);
var sex = parameter.split("=")[1];
switch (sex) {
    case "m":
        console.log("Male");
        break;
    case "f":
        console.log("Female");
        break;
    default:
        console.log("Unknown");
}
```


### for	

```javascript
let weeks = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];

for (let i = 0; i < weeks.length; i++) {
    console.log(weeks[i]);
}

for (let day in weeks) {
    console.log(day);
}

for (let day of weeks) {
    console.log(day);
}
```


### while

```javascript
let weeks = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
let i = 0;

while (i < weeks.length) {
    console.log(weeks[i++]);
}
```


### do

```javascript
let weeks = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
let i = 0;

do {
    console.log(weeks[i++]);
} while (i < weeks.length);
```


### forEach 

```javascript
let weeks = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];

weeks.forEach(function (element, index) {
   console.log(element, index);
});

weeks.forEach((element, index) => {
    console.log(element, index);
});
```


---

## Function


```javascript
// function declaration or named function or defined function
function sayHi(arg) { return "Hi " + arg; }
console.log(sayHi("JS"));

// function expression or anonymous function
let sayGood = function(arg) { return "Good " + arg; };
console.log(sayGood("JS"));

// arrow function
// arrow function 沒有 prototype, 所以無法使用 new, 也無法變更 this 的內容
const sayNice = (arg) => { return "Nice " + arg; };
const sayNice2 = arg => { return "Nice " + arg; };
const sayNice3 = () => { return "Nice JS"; };
const sayNice4 = () => "Nice JS";
console.log(sayNice("JS"));
console.log(sayNice2("JS"));
console.log(sayNice3());
console.log(sayNice4());

// function constructor
let sayHello = new Function("arg", "return \"Hello \"+ arg;");
console.log(sayHello("JS"));

// closure function
let countNumber = function () {
    let count = 0; // count在countNumber裡的區域變數
    return function () {
        return count += 1;
    }
};
console.log(countNumber());    // Function
console.log(countNumber()());  // 1
console.log(countNumber()());  // 1

const c = countNumber();
console.log(c());              // 1
console.log(c());              // 2

// partial function, currying function
function multiplier(factor) {
    return number => number * factor;
}
const twice = multiplier(2);
console.log(twice(10));
```


### parameter

```javascript
// default parameter
var f0 = function (arg = "JavaScript") {
    return `Hello ${arg}`;
};

var f1 = f0;    // function reference
var f2 = f0();  // function call/invoke

console.log(f0);
console.log(f1);
console.log(f2);

console.log(f0());
console.log(f1());
// console.log(f2());

// rest parameter
function cast(a, b, ...others) {
    console.log(`a: ${a}`);
    console.log(`b: ${b}`);
    console.log(`others: ${others}`);
}

cast(1,2,3);
cast(1,2,3,4,5);
cast(1,2);

// parameter with object destructure
function m1({x = 0, y = 0} = {}) {
    return [x, y];
}

function m2({x, y} = { x: 0, y: 0 }) {
    return [x, y];
}

m1();
m2();

m1({x: 3, y: 8});
m2({x: 3, y: 8});

m1({x: 3});
m2({x: 3});

m1({});
m2({});

m1({z: 3});
m2({z: 3});

// arguments
function noArg(arg0) {
    console.log(`arguments.length: ${arguments.length}`);
    console.log(`args0: ${arg0}, arguments[0]: ${arguments[0]}`);
    console.log(`arguments[1]: ${arguments[1]}`);
}

noArg('a', 'b');
```


### this

```javascript
const o = {
    name: "property",
    showMessage: function () {
        console.log(`Hi ${this.name}`);
    },
    showThis: function () {
        let that = this.name;
        let anonymous = function () {
            console.log(`anonymous this: ${this.name}`);
            console.log(`anonymous that: ${that}`);
        };
        let arrow = () => {
            console.log(`arrow this: ${this.name}`);
            console.log(`arrow that: ${that}`);
        };

        anonymous();
        arrow();
    }
};

console.log(o.name);                  // property
console.log(o.showMessage());         // Hi property
                                      // undefined
console.log(o.showThis());            // anonymous this: undefined
                                      // anonymous that: property
                                      // arrow this: property
                                      // arrow that: property
                                      // undefined

name = "global";
let msg = o.showMessage;
msg();                                // Hi global
```

```javascript
// this for function
function ninja() {
    return this;
}

function samurai() {
    "use strict";
    return this;
}

let fExpress = function() {return this};

let fArrow = () => {return this};

// console.log(ninja() === window);  // run on browser
console.log(ninja() === global);     // run on nodejs, but es6 module false, common js ture
console.log(samurai() === undefined);
console.log(fExpress() === global);  // run on nodejs, but es6 module false, common js ture
console.log(fArrow() === undefined);

// this for object
const objThis = {
    ninja: ninja,
    samurai: samurai
};
console.log(objThis.ninja() === objThis);
console.log(objThis.samurai() === objThis);

// this for constructor function
function FnThis() {
    this.ninja = ninja;
    this.samurai = samurai;
}
let fnThis = new FnThis();
console.log(fnThis.ninja() === fnThis);
console.log(fnThis.samurai() === fnThis);
```


### apply, call, bind

```javascript
function addOne(a) {
    return a + 1;
}
console.log(addOne(1));

function add(a, b) {
    return a + b;
}
let add1 = add.bind(null, 1);  // partial function
console.log(add1(1));
```

```javascript
// apply, call ,bind for function without this
function sum1() {
    let total = 0;
    for (let i = 0; i < arguments.length; i++) {
        total += arguments[i];
    }
    return total;
}

console.log(`fn:       ${sum1(1, 2, 3)}`);                // invoke
console.log(`fn.apply: ${sum1.apply(null, [1, 2, 3])}`);  // apply
console.log(`fn.call:  ${sum1.call(null, 1, 2, 3)}`);     // call
console.log(`fn.bind:  ${sum1.bind(null, 1, 2, 3)()}`);   // bind

// apply, call ,bind for function with this
function sum2() {
    let total = 0;
    for (let i = 0; i < arguments.length; i++) {
        total += arguments[i];
    }
    this.result = total;
    return total;
}

let sFn = new sum2(1, 2, 3);
let oApply = {};
let oCall = {};
let oBind = {};
console.log(`fn:       ${sFn}, ${sFn.result}`);                               // function construtor
console.log(`fn.apply: ${sum2.apply(oApply, [1, 2, 3])}, ${oApply.result}`);  // apply
console.log(`fn.call:  ${sum2.call(oCall, 1, 2, 3)}, ${oCall.result}`);       // call
console.log(`fn.bind:  ${sum2.bind(oBind, 1, 2, 3)()}, ${oBind.result}`);     // bind
```

---

## Class


### function

```javascript
// function before ES5
function Car0(make, model) {
    // member
    this.make = make;
    this.model = model;
    this._userGears = ['P', 'N', 'R', 'D'];
    this._userGear = this._userGears[0];

    // method
    this.userGear = function () {
        return this._userGear;
    };

    // initialize
    if ( typeof Car0.number == 'undefined' ) {
        // static member
        Car0.number = 0;
    }
    Car0.count = function (){
        Car0.number++;
    };
    // static method
    Car0.count();
}
// dynamic bind method
// anti pattern
Car0.prototype.shift = function (gear) {
        this._userGear = gear;
};

let car0 = new Car0("Tesla", "Model S");
console.log(car0._userGear);
console.log(car0.userGear());
car0.shift('D');
console.log(car0.userGear());

console.log(Car0.number);
Car0.count();
console.log(Car0.number);
```


### class

```javascript
class Car1 {
    constructor(make, model) {
        this.make = make;
        this.model = model;
        this._userGears = ['P', 'N', 'R', 'D'];
        this._userGear = this._userGears[0];
        Car1.count();
    }

    get userGear() {
        return this._userGear;
    }

    set userGear(value) {
        if (this._userGears.indexOf(value) < 0) {
            throw new Error(`Invalid gear: ${value}`);
        }
        this._userGear = value;
    }

    shift(gear) {
        this.userGear = gear;
    }

    static count() {
        Car1.number ++;
    }
}
Car1.number = 0;

let car1 = new Car1("Tesla", "Model S");
console.log(car1._userGear);
console.log(car1.userGear);
car1.shift('D');
console.log(car1.userGear);
car1.userGear = 'R';
console.log(car1.userGear);
car1._userGear = 'P';
console.log(car1.userGear);

console.log(Car1.number);
Car1.count();
console.log(Car1.number);
```


### extends

```javascript
class Vehicle {
    constructor() {
        this.passengers = [];
        console.log("create vehicle");
    }
    addPasseneger(p) {
        this.passengers.push(p)
    }
}

class Car extends Vehicle {
    constructor() {
        super();
        console.log("create car");
    }
    deployAirBag() {
        console.log("air bag");
    }
}

const v = new Vehicle();
v.addPasseneger("John");
console.log(v.passengers);

const c = new Car();
c.addPasseneger("Mary");
console.log(c.passengers);
c.deployAirBag();

class Moto extends Vehicle {}
const m = new Moto();

console.log(`m instanceof Vehicle: ${m instanceof Vehicle}`);
console.log(`m instanceof Car: ${m instanceof Car}`);
console.log(`m instanceof Moto: ${m instanceof Moto}`);
```


### mixin

```javascript
class InsurancePolicy {}
function makeInsurable(o) {
    o.addInsurancePolicy = function (p) { this.insurancePolicy = p; };
    o.getInsurancePolicy = function () { return this.insurancePolicy; };
    o.isInsured = function () { return !!this.insurancePolicy; };
}

let insurance = new InsurancePolicy();
insurance.tax = 10;

// method 1
const car1 = new Car();
makeInsurable(car1);
car1.addInsurancePolicy(insurance);
console.log(car1.getInsurancePolicy());


// method 2
makeInsurable(Car.prototype);
const car1 = new Car();
car1.addInsurancePolicy(insurance);
console.log(car1.getInsurancePolicy());
```


### function map to class

```javascript
function NinjaFn(name, level) {
    this.name = name;                            // public field
    let _level = level;                          // private field

    this.getLevel = function () {
        return _level;
    }
    this.setLevel = function(level) {
        _level = level;
    }
}
// NinjaFn.prototype.swingSword = function() {      // public method
//     return true;
// }
NinjaFn.prototype = {
    swingSword: function() {                     // public method
        return true;
    }
}
NinjaFn.compare = function(ninja1, ninja2) {     // static method
    return ninja1.getLevel() - ninja2.getLevel();
}

let ninjaFn1 = new NinjaFn('ninjaFn1', 5);
let ninjaFn2 = new NinjaFn('ninjaFn2', 1);
console.log(`${ninjaFn1.name}, ${ninjaFn1._level}, ${ninjaFn1.getLevel()}`);
console.log(`${ninjaFn2.name}, ${ninjaFn2.swingSword()}`);
console.log(`NinjaFn.compare:  ninjaFn  - ninjaFn  = ${NinjaFn.compare(ninjaFn1, ninjaFn2)}`);


class NinjaCls {
    constructor(name, level) {
        this.name = name;                        // public field
        let _level;                              // private field

        this.getLevel = function () {
            return _level;
        }
        this.setLevel = function(level) {
            _level = level;
        }

        this.setLevel(level);
    }

    swingSword() {                               // public method
        return true;
    }

    static compare(ninja1, ninja2) {             // static method
        return ninja1.getLevel() - ninja2.getLevel();
    }
}

let ninjaCls1 = new NinjaCls('ninjaCls1', 5);
let ninjaCls2 = new NinjaCls('ninjaCls2', 1);
console.log(`${ninjaCls1.name}, ${ninjaCls1._level}, ${ninjaCls1.getLevel()}`);
console.log(`${ninjaCls2.name}, ${ninjaCls2.swingSword()}`);
console.log(`NinjaCls.compare: ninjaCls - ninjaCls = ${NinjaCls.compare(ninjaCls1, ninjaCls2)}`);


console.log(`NinjaFn.compare:  ninjaCls - ninjaCls = ${NinjaFn.compare(ninjaCls1, ninjaCls2)}`);
console.log(`NinjaCls.compare: ninjaFn  - ninjaFn  = ${NinjaCls.compare(ninjaFn1, ninjaFn2)}`);
```

### function map to extends

```javascript
function extend(base, sub) {
    var origProto = sub.prototype;
    sub.prototype = Object.create(base.prototype);
    for (var key in origProto)  {
        sub.prototype[key] = origProto[key];
    }

    Object.defineProperty(sub.prototype, 'constructor', { 
        enumerable: false,
        value: sub
    });
}

function PersonFn(name) {
    this.name = name;
}
PersonFn.prototype.dance = function() {
    return true;
}

function NinjaFn(name, weapon) {
    PersonFn.call(this, name);
    this.weapon = weapon;
}
NinjaFn.prototype = {
    wieldWeapon: function() {
        return this.weapon;
    }
}

extend(PersonFn, NinjaFn);


const personFn = new PersonFn('PersonFn');
const ninjaFn = new NinjaFn('NinjaFn', 'wakizashi');

console.log(`personFn instanceof PersonFn: ${personFn instanceof PersonFn}`);
console.log(`personFn instanceof NinjaFn:  ${personFn instanceof NinjaFn}`);
console.log(`ninjaFn  instanceof NinjaFn:  ${ninjaFn instanceof NinjaFn}`);
console.log(`ninjaFn  instanceof PersonFn: ${ninjaFn instanceof PersonFn}`);
console.log(ninjaFn.name);
console.log(ninjaFn.dance())


class PersonCls {
    constructor(name) {
        this.name = name;
    }

    dance() {
        return true;
    }
}

class NinjaCls extends PersonCls {
    constructor(name, weapon) {
        super(name);
        this.weapon = weapon;
    }

    wieldWeapon() {
        return this.weapon;
    }
}

const personCls = new PersonCls('personCls');
const ninjaCls = new NinjaCls('ninjaCls', 'wakizashi');

console.log(`personCls instanceof PersonCls: ${personCls instanceof PersonCls}`)
console.log(`personCls instanceof NinjaCls:  ${personCls instanceof NinjaCls}`)
console.log(`ninjaCls  instanceof NinjaCls:  ${ninjaCls instanceof NinjaCls}`)
console.log(`ninjaCls  instanceof PersonCls: ${ninjaCls instanceof PersonCls}`)
console.log(ninjaCls.name);
console.log(ninjaCls.dance())
```


---

## Exception


### try / catch / finally

```javascript
var validateEmail = function(email) {
  return email.match(/@/) ? email : new Error(`invalid email ${email}`);
};

// const email = "abc@dot.net";
// const email = "dot.net";
const  email = null;

try {
    const res = validateEmail(email);
    if (res instanceof Error) {
        console.error(`Error ${res}`);
    } else {
        console.log(`Validate email ${email}`);
    }
} catch (e) {
    console.error(`Error ${e.message}`);
} finally {
    console.log(`Always do it`);
}
```


### throw

```javascript
let div = function (a, b) {
    if (b === 0) {
        throw new Error(`b isn't 0`);
    }
    return a / b
};

try {
    console.log(div(1, 1));
    // console.log(div(1, 0));
} catch (e) {
    console.error(e.message);
}

console.log(div(1, 0));
```


---

## Iterator


### iterator

```javascript
const weeks = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
const it = weeks.values();   // array -> iterator
let current = it.next();     // get iterator value

while (!current.done) {
    console.log(current);
    current = it.next();
}
```


### iterable protocol

```javascript
class Log {
    constructor() {
        this.messages= [];
    }
    add(message) {
        this.messages.push({message, timestamp: Date.now()});
    }
    [Symbol.iterator]() {
        return this.messages.values()
    }
}

const log = new Log();
log.add("create api");
log.add("update api");
log.add("update api");

for (let entry of log) {
    console.log(`${entry.message} @ ${entry.timestamp}`);
}
```


### iterator protocol

```javascript
class Log {
    constructor() {
        this.messages= [];
    }
    add(message) {
        this.messages.push({message, timestamp: Date.now()});
    }
    [Symbol.iterator]() {
        let i = 0;
        const messages = this.messages;
        return {
            next() {
                if(i >= messages.length) {
                    return { value: undefined, done: true}
                } else {
                    return { value: messages[i++], done: false}
                }
            }
        }
    }
}

const log = new Log();
log.add("create api");
log.add("update api");
log.add("update api");

for (let entry of log) {
    console.log(`${entry.message} @ ${entry.timestamp}`);
}
```

### get, set

```javascript
class NinjaClsCollection {
    constructor() {
        this.ninjas = ["Yoshi", "Kuma", "Hattori"];
    }

    get first() {
        return this.ninjas[0];
    }

    set first(ninja) {
        this.ninjas[0] = ninja
    }
}

let ninjaClsCollection = new NinjaClsCollection()
console.log(`cls get: ${ninjaClsCollection.first}`);
ninjaClsCollection.first = "Hachi";
console.log(`cls set: ${ninjaClsCollection.first}`);


function NinjaFnCollection() {
    this.ninjas = ["Yoshi", "Kuma", "Hattori"];

    Object.defineProperty(this, "first", {
        get: () => {
            return this.ninjas[0];
        },
        set: (ninja) => {
            this.ninjas[0] = ninja;
        }
    });
}

let ninjaFnCollection = new NinjaFnCollection()
console.log(`fn get: ${ninjaFnCollection.first}`);
ninjaFnCollection.first = "Hachi";
console.log(`fn set: ${ninjaFnCollection.first}`);
```

---

## Generator


### yield

```javascript
const rainbow = function* () {
    yield "red";
    yield "orange";
    yield "yellow";
    yield "green";
    yield "blue";
    yield "indigo";
    yield "violet";
};

for (let color of rainbow()) {
    console.log(color);
}
```

### return

```javascript
const abc = function* () {
    yield "a";
    yield "b";
    return "c";
};

for (let c of abc()) {
    console.log(c);
}

const it = abc();
console.log(it.next());
console.log(it.next());
console.log(it.next());
```


### next

```javascript
const interrogate = function* () {
    const name = yield "who's your name?";
    const color = yield "what's your favorite color?";
    return `${name}'s favorite color is ${color}`;
};

const it = interrogate();
console.log(it.next());
console.log(it.next("Joe"));
console.log(it.next("red"));
```


---

## Async

### call back

```javascript
function countdown(s) {
    var i;
    for (i = s; i >= 0; i--) {
        setTimeout(function () {
            console.log(i === 0 ? "go!" : i);
        }, ((s - i) * 1000));
    }
}

countdown(5);
```

`IIFE`

Immediately Invoked Function Expression

```javascript
function countdown(s) {
    var i;
    for (i=s; i>=0; i--) {
        (function(i) {
            setTimeout(function () {
                console.log(i === 0 ? "go!" : i);
            }, ((s - i) * 1000));
        })(i);
    }
}

countdown(5);
```

`scope`

```javascript
function countdown(s) {
    for (let i=s; i>=0; i--) {
        setTimeout(function () {
            console.log(i === 0 ? "go!" : i);
            }, ((s - i) * 1000));
        }
}

countdown(5);
```

`call back hell`


### promise

```javascript
function countdown(s) {
    return new Promise(function (resolve, reject) {
        for (let i = s; i >= 0; i--) {
            setTimeout(function () {
                i === 0 ? resolve(console.log("go!")) : console.log(i)
            }, (s - i) * 1000);
        }
    });
}

countdown(5).then();

countdown(5).then(
    function () {
        console.log("countdown successful");
    },
    function (err) {
        console.log("countdown fail" + err.message);
    }
);
```

```javascript
var promise = new Promise(function(resolve, reject) {
  // do a thing, possibly async, then…

  if (/* everything turned out fine */) {
    resolve("Stuff worked!");
  }
  else {
    reject(Error("It broke"));
  }
});

promise.then(function(result) {
  console.log(result); // "Stuff worked!"
}, function(err) {
  console.log(err); // Error: "It broke"
});
```


### co -> sequence run

```javascript
function* seqRun() {
    try {
        yield countdown(5);
        console.log("countdown successful");
    } catch (err) {
        console.log("countdown fail" + err.message);
    }
}

for (let f of seqRun()) {
    f;
}
```

```javascript
let co = require('co');

co(function *() {
    try {
        yield countdown(5);
        console.log("countdown successful");
    } catch (err) {
        console.log("countdown fail" + err.message);
    }
});
```


### async / await

```javascript
async function aRun() {
    try {
        await countdown(5);
        console.log("countdown successful");
    } catch (err) {
        console.log("countdown fail" + err.message);
    }
}

aRun();
```


---

## Regex

```javascript
const re1 = /going/;
const re2 = new RegExp("going");
const sta = "As I was going to movie";

console.log(sta.match(re1));
console.log(sta.search(re1));

console.log(sta.match(re2));
console.log(sta.search(re2));

console.log(re1.test(sta));
console.log(re1.exec(sta));
```

```javascript
var str = '/usr/lib/python2.6/site-packages/gtk-2.0/gconf.so'; 
console.log(str); 

// match進行比對，回傳匹配字串array 
// search進行比對，回傳匹配字串position；indexOF不能用於RE 
// replace進行比對，將匹配字串修改且回傳 
// 將要匹配字串放入/pattern/之中 

var re = /(.*)\.(.*?)$/; // RE宣告，將pattern夾在//之中但不適用於變數 
var restr = str.match(re); 
console.log(restr[1] + "<=>" + restr[2]); 
console.log(str.search(re)); 
console.log(str.replace(/.[^.]*$/, '')); // 不修改str內容，但修改回傳值 

var re = new RegExp(/(.*?)\.(.*)$/); // 另一種RE宣告，適用於變數 
var restr = str.match(re); 
console.log(restr[1] + "<=>" + restr[2]); 
console.log(str.search(re)); 
console.log(str.replace(/\.(.*)$/, '')); 

var re = /(.*?)\/(.*)$/; 
var restr = str.match(re); 
console.log(restr[1] + "<=>" + restr[2]); 
console.log(str.search(re)); 
console.log(str.replace(/(.*?)\//, '')); 

var re = /(.*)\/(.*)$/; 
var restr = str.match(re); 
console.log(restr[1] + "<=>" + restr[2]); 
console.log(str.search(re)); 
console.log(str.replace(/(.*)\//, '')); 
```


### capturing

`syntax`

```
(subexpression)
```

```javascript
const text = "Visit oreilly.com today";
const re = /[a-z]+(\.com|\.org|\.edu)/;

console.log(text.match(re));
console.log(text.replace(re, "\n$$&: ($&)\n$$1: ($1)\n$$`: ($`)\n$$: ($$)\n$$':($')\n"));
```

```javascript
const t = "ABCDEDCBABCDE";

const r1 = /(C).*C/;
const r2 = /(C).*?C/;
console.log(t.match(r1));
console.log(t.match(r2));

const r3 = /(C).*\1/;
const r4 = /(C).*?\1/;
console.log(t.match(r3));
console.log(t.match(r4));
```


### non capturing

`syntax`

```
(?:subexpression)
```

```javascript
const text = "Visit oreilly.com today";
const re = /[a-z]+(:?\.com|\.org|\.edu)/;

console.log(text.match(re));
console.log(text.replace(re, "\n$$&: ($&)\n$$1: ($1)\n$$`: ($`)\n$$: ($$)\n$$':($')\n"));
```

```javascript
const t = "ABCDEDCBABCDE";

const r1 = /(:?C).*C/;
const r2 = /(:?C).*?C/;
console.log(t.match(r1));
console.log(t.match(r2));

const r3 = /(:?C).*\1/;
const r4 = /(:?C).*?\1/;
console.log(t.match(r3));
console.log(t.match(r4));
```


### lookahead

`syntax`

```
(?=subexpression)
(?!subexpression)
```

```javascript
function validPassword1(p) {
    return /[A-Z]/.test(p) &&
        /[0-9]/.test(p) &&
        /[a-z]/.test(p) &&
        !/[^a-zA-Z0-9]/.test(p);
}

function validPassword2(p) {
    return /[A-Z].*[0-9][a-z]/.test(p);
}

function validPassword3(p) {
    return /(?=.*[A-Z])(?=.*[0-9])(?=.*[a-z])(?!.*[^a-zA-Z0-9])/.test(p);
}

const p1 = 'xyzABC123';
const p2 = 'ABCxyz123';
const p3 = 'ABC123xyz';

console.log(validPassword1(p1));
console.log(validPassword2(p1));
console.log(validPassword3(p1));

console.log(validPassword1(p2));
console.log(validPassword2(p2));
console.log(validPassword3(p2));

console.log(validPassword1(p3));
console.log(validPassword2(p3));
console.log(validPassword3(p3));
```


---

## DOM event

```html
<!DOCTYPE html>
<html>
<head>
    <title>DOM Event</title>
</head>
<body>

<!-- inline model -->
<button id="button1" onclick="console.log('Hello Button1!');">Button1</button><br />
<button id="button2" onclick>Button2</button><br />
<button id="button3" onclick>Button3</button><br />


<script type="text/javascript">
// traditional model
document.getElementById('button2').onclick = function(){
    console.log('Hello Button2!')
}

// even listener
const el = document.getElementById('button3')
el.addEventListener( 'click', function(){
     console.log('Helloo Button3!')
}, false)
</script>

</body>
</html>
```


---

## Reference

[JAVASCRIPT.INFO](https://javascript.info/)

[Javascript Tutorial](https://www.tutorialspoint.com/javascript/index.htm)

[JavaScript Tutorial](https://www.w3schools.com/js/)
