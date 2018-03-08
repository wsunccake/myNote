# JavaScript #

## Introduction

1995 年 Netscape 的 Brendan Eich 設計出 JavaScript (原名為 LiveScript, 為了與昇陽合作, 搭上 Java 的順風車, 改名為 JavaScript), 加入到 Netscape 2.0 瀏覽器中, 因而成為瀏覽器的共通語言. JavaScript 是一種原型導向的語言, 具有動態與弱型別等特性, 後來各家瀏覽器紛紛支援, 但是由於實作方式和語法都不統一 (JavaScript 同時存在: Netscape Navigator 3.0 的 JavaScript, IE 中的 JScript 以及 CEnvi 中的 ScriptEase), 因此造成了混亂的狀況, 於是在 1998 年提交到 ECMA 組織制訂成 ECMA Script 的標準, 以便統一 JavaScript 的語法.  
Web 2.0 的風潮進一步刺激了 JavaScript 的廣泛使用, 許多網站利用 AJAX 的 JavaScript 技術達成了高度的網頁互動性, 像是 Google Map 就是其中最著名的網站. 在 HTML5 的草案提出之後, JavaScript 更受到高度的重視, 由於 HTML5 的強大功能, 讓大家對 JavaScript 的發展充滿了信心, 很多人認為 JavaScript 將會是繼 C 之後最重要的程式語言.
JavaScript 一開始發展是在瀏覽器上, 所以在只能在瀏覽器執行, 可是不利於在終端機下直接在使用. 在 1997 年, [Rhino](https://developer.mozilla.org/en-US/docs/Mozilla/Projects/Rhino) 專案以 Java 開發了可以在終端機下執行的 JavaScript Engine. 在 2009 年, [Node.js](https://nodejs.org/) 基於 Google 的 V8 JavaScript Engine.

執行 JavaScript 範例

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

---

## Data Type

JavaScript 中的變數分為 numerical, string, boolean 和 object type 有 array, object, resource, NULL. 變數宣告要使用 var (沒宣告 var 也可以, 但變數會成為全域變數), 變數名稱的開頭必須是底線（_）或英文字母, 英文字母的大小寫都可以, 而且大小寫有別, 要注意數字不可以作為變數的開頭.


### String

```js
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

```js
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

```js
// 0 or Nan is false, 1 is true
var bl1 = true;

// 轉Boolean 
Boolean(str3); 
!!num1;
```

### Array

```js
// array to string
["do", "re", "mi"].join(" ");
```

### Object
	
	// String 處理
	str1.toLowerCase();
	str2.toUpperCase();
	" lorem ".trim();
	" lorem".trimLeft();
	"lorem ".trimRight();
	"lorem ipsum".substr(6, 5);
	"value: " + 8;

	"do re mi".split(" "); // string轉array
	

`object`


	

	
	// 定義全域變數 
	var MYGLOBAL = {} || MYGLOBAL;
	MYGLOBAL.var1 = "xyz";
	MYGLOBAL.var2 = 123;


---

## Reference

[JAVASCRIPT.INFO](https://javascript.info/)

[Javascript Tutorial](https://www.tutorialspoint.com/javascript/index.htm)

[JavaScript Tutorial](https://www.w3schools.com/js/)
