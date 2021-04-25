# prototype

```javascript
// object
let obj1 = {};
let obj2 = new Object();

console.log(`obj1: ${Object.getPrototypeOf(obj1) === Object.prototype}`);
console.log(`obj2: ${Object.getPrototypeOf(obj2) === Object.prototype}`);

// class
function Person(name) {
    this.name = name;
};
Person.prototype.getName = function() {
    return this.name;
};

let p = new Person('js');
console.log(`field: ${p.name}`);
console.log(`method: ${p.getName()}`);
console.log(`prototype: ${Object.getPrototypeOf(p) === Person.prototype}`);

// inherit
function A() {};
A.prototype = { 
    name: 'js',
    getName: function() { return this.name; }
};
A.hello = function() { return `Hi ${this.name}`; };

function B() {};
B.prototype = new A();

function C() {};
C.prototype = Object.create(new A());

let a = new A();
console.log(`a: ${a.name}, ${a.getName()}`);
console.log(`a instanceof A: ${a instanceof A}`);

let b = new B();
console.log(`b: ${b.name}, ${b.getName()}`);
console.log(`b instanceof B: ${b instanceof B}`);
console.log(`b instanceof A: ${b instanceof A}`);
console.log(`b instanceof C: ${b instanceof C}`);

let c = new C();
console.log(`c: ${c.name}, ${c.getName()}`);
console.log(`c instanceof C: ${c instanceof C}`);
console.log(`c instanceof A: ${c instanceof A}`);
console.log(`c instanceof B: ${c instanceof B}`);

// function
Object.create = Object.create || function(obj) {
    let F = function() {};
    F.prototype = obj;
    return new F();
}
```

---

# this

```javascript
// window.name = 'GLOBAL NAME';      // for browser
global.name = 'GLOBAL NAME';         // for node js
// globalThis.name = 'GLOBAL NAME';


const fn0 = function() {
    if (typeof this !== 'undefined') { console.log(`this: ${this}`); }
    if (typeof self !== 'undefined') { console.log(`self: ${self}`); }
    if (typeof window !== 'undefined') { console.log(`window: ${window}`); }
    if (typeof global !== 'undefined') { console.log(`global: ${global}`); }
    if (typeof globalThis !== 'undefined') { console.log(`globalThis: ${globalThis}`); }
};
fn0();

const obj0 = {name: 'obj name'}


// function
const fn1 = function() {
    return this.name;
};
console.log(`fn1 this.name: ${fn1()}`);
console.log(`fn1 apply this.name: ${fn1.apply(null, [])}`);
console.log(`fn1 call this.name: ${fn1.call(null)}`);
console.log(`fn1 bind this.name: ${fn1.bind(null)()}`);
console.log(`fn1 apply this.name: ${fn1.apply(obj0, [])}`);
console.log(`fn1 call this.name: ${fn1.call(obj0)}`);
console.log(`fn1 bind this.name: ${fn1.bind(obj0)()}`);


// object
const obj1 = {
    name: 'obj name',
    getName: function() {
        return this.name;
    } 
};
console.log(`obj1 getName: ${obj1.getName()}`);
console.log(`obj1 this.name: ${obj1.name}`);


// function
const fn2 = obj1.getName;
console.log(`fn2 this.name: ${fn2()}`);


// constructor
const FunClass1 = function() {
    this.name = 'fun class name';
    return {
        name: 'fun name'
    }
};
const fc1 = new FunClass1();
console.log(`fc1 this.name: ${fc1.name}`);

const FunClass2 = function() {
    this.name = 'fun class name';
    return 'fun name';
};
const fc2 = new FunClass2();
console.log(`fc2 this.name: ${fc2.name}`);
```

