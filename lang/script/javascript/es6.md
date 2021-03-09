# ES 6

## Introduction

ECMAScript (European Computer Manufacturers Association)


---

## Template Literal

```javascript
var name = "JavaScript";
var text = `Hello ${name}`;
console.log(text);

`Now: ${new Date(),toLocaleString()}`;
`2+3: ${2 + 3}`;

console.log(String.raw `"\n"Hello ${name}`);
```


---

## Object Literal

`object`

```javascript
// ES 5
var listeners = [];
function listen() {}
var events =  {
    listeners: listeners,
    listen: listen
};

console.log(events.listeners);
console.log(events.listen);

// ES 6
var listeners = [];
function listen() {}
var events =  {
    listeners,
    listen
};

console.log(events.listeners);
console.log(events.listen);
```

`object of function`

```javascript
// ES 5
function getEnvelope(type, description) {
  var envelope = {
      data: {}
  };
  envelope[type] = description;
  return envelope;
}
console.log(getEnvelope('a', 'aAa'));

// ES 6
function getEnvelope(type, description) {
    return {
        data: {},
        [type]: description
    };
}
console.log(getEnvelope('a', 'aAa'));
```

`function of object`

```javascript
// ES 5
var emiter = {
  events: {},
  on: function (type, fn) {
    if (this.events[type] === undefined) {
        this.events[type] = [];
    }
    this.events[type].push(fn);
  },
  emit: function (type, event) {
    if (this.events[type] === undefined) {
        return ;
    }
    this.events[type].forEach(function (fn) {
        fn(event);
    })
  }
};

emiter.on('sayHi', function (event) {
 console.log("Hi " + event);
});

emiter.emit('sayHi', 'JS');

// ES 6
var emiter = {
  events: {},
  on(type, fn) {
    if (this.events[type] === undefined) {
        this.events[type] = [];
    }
    this.events[type].push(fn);
  },
  emit(type, event) {
    if (this.events[type] === undefined) {
        return ;
    }
    this.events[type].forEach(function (fn) {
        fn(event);
    })
  }
};

emiter.on('sayHi', function (event) {
  console.log("Hi " + event);
});

emiter.emit('sayHi', 'JS');
```


---

## Arrow Functions

arrow function 沒有 prototype, 所以無法使用 new, 也無法變更 this 的內容

```javascript
// define function
function name(param) {
	...
}

// anonymous function
var anonymous = function(param) {
	...
}

// arrow function
var arrow = (param) => {
	...
}
```

```javascript
var timer = {
    second: 0,
    start() {
        setInterval(() => {
            this.second++
        }, 1000)
    }
};

timer.start();
setTimeout(function () {
    console.log(timer.second);
}, 3000);

```

---

## Default Parameter

```javascript
// ES 5
var link = function (height, color) {  
  var height = height || 50;  
  var color = color || 'red';
  ...
}

// ES 6
var link = function (height = 50, color = 'red') {  
   ...
}
```


---

## Spread Operator

`array`

```javascript
console.log([1, ...[2, 3], 4]);
```

`function`

```javascript
function cast() {
  return [...arguments]
}

console.log(cast(1,2,3));
console.log(cast([1,2,3]));
```


---

## Destructuring Assignment

```javascript
var names1 = ["James", "L.", "Howlett"];
var [firstname1, , lastname1] = names1;
var [firstname2 = "John", , lastname2 = "Doe"] = names1;

var right = 1;
var left = 2;
[right, left] = [left, right];

[a, b, ...other] = [1, 2, 3, 4, 5];

```


---

## Class


---

## Module

### common js

```javascript
// m.js 
exports.PI = 3.14;

// main.js
const m = require('./m.js');
console.log(m.PI);

// main.js
const m = require('./m.js');
const {PI: pi} = m;
console.log(pi);

// main.js
const { PI } = require('./m.js');
console.log(PI);

// main.js
const m = require('./m.js');
const { PI } = m;
console.log(PI);
```


### es module

```javascript
// m.js
export default {
  PI: 3.14
};

// main.js
import m from './m.js';
console.log(m.PI);

// main.js
import m from './m.js';
const { PI } = m
console.log(PI);

// main.js
import m from './m.js';
const { PI: pi } = m
console.log(PI: pi);
```

```javascript
// m.js
export const PI = 3.14;

// main.js
import { PI } from './m.js';
console.log(PI);
```


---

## Reference

[ES6 標準入門](http://es6.ruanyifeng.com/)
