# JavaScript #

## Introduction

1995 年 Netscape 的 Brendan Eich 設計出 JavaScript (原名為 LiveScript, 為了與昇陽合作, 搭上 Java 的順風車, 改名為 JavaScript), 加入到 Netscape 2.0 瀏覽器中, 因而成為瀏覽器的共通語言. JavaScript 是一種原型導向的語言, 具有動態與弱型別等特性, 後來各家瀏覽器紛紛支援, 但是由於實作方式和語法都不統一 (JavaScript 同時存在: Netscape Navigator 3.0 的 JavaScript, IE 中的 JScript 以及 CEnvi 中的 ScriptEase), 因此造成了混亂的狀況, 於是在 1998 年提交到 ECMA 組織制訂成 ECMA Script 的標準, 以便統一 JavaScript 的語法.  
Web 2.0 的風潮進一步刺激了 JavaScript 的廣泛使用, 許多網站利用 AJAX 的 JavaScript 技術達成了高度的網頁互動性, 像是 Google Map 就是其中最著名的網站. 在 HTML5 的草案提出之後, JavaScript 更受到高度的重視, 由於 HTML5 的強大功能, 讓大家對 JavaScript 的發展充滿了信心, 很多人認為 JavaScript 將會是繼 C 之後最重要的程式語言.
JavaScript 一開始發展是在瀏覽器上, 所以在只能在瀏覽器執行, 可是不利於在終端機下直接在使用. 在 1997 年, [Rhino](https://developer.mozilla.org/en-US/docs/Mozilla/Projects/Rhino) 專案以 Java 開發了可以在終端機下執行的 JavaScript Engine. 在 2009 年, [Node.js](https://nodejs.org/) 基於 Google 的 V8 JavaScript Engine.

執行 JavaScript 範例

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

`Node.JS`

```bash
# REPL
linux:~ # node
> console.log('Hello JavaScript');
> process.exit()

# command
linux:~ # node -e 'console.log("Hello, %s", "Nodejs");'
linux:~ # echo 'console.log("Hello NodeJS");' | node -i

# script
linux:~ # cat helle.js
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

## Variable

### var

```javascript
var var1 = 123;
var var2;
```

### let

```javascript
for (let i in [1, 2, 3]) {
    console.log(i);
}
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
for (let char of "Hello") {console.log(char);}
for (let char in "Hello") {console.log(char);}

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
```

```javascript
// 定義全域變數 
var MYGLOBAL = {} || MYGLOBAL;
MYGLOBAL.var1 = "xyz";
MYGLOBAL.var2 = 123;
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


### while


---

## Function

---

## Reference

[JAVASCRIPT.INFO](https://javascript.info/)

[Javascript Tutorial](https://www.tutorialspoint.com/javascript/index.htm)

[JavaScript Tutorial](https://www.w3schools.com/js/)
