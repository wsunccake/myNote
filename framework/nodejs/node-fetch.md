# node-fetch

```bash
[linux:~ ] $ mkdir project
[linux:~ ] $ cd project
[linux:project ] $ npm init
[linux:project ] $ npm install node-fetch
[linux:project ] $ npm list
[linux:project ] $ npm info node-fetch
```

```javascript
const fetch = require("node-fetch");

const url = "https://github.com/";
fetch(url)
  .then((res) => res.text())
  .then((body) => console.log(body));
```

---

## for common js

```bash
[linux:project ] $ vi package.json
{
    "type": "commonjs"
}
```

```javascript
const fetch = require("node-fetch");

const url1 = "https://github.com/";
fetch(url1)
  .then((res) => res.text())
  .then((body) => console.log(body));

const url2 = "https://api.github.com/users/github";
fetch(url2)
  .then((res) => res.json())
  .then((json) => console.log(json));

const url3 = "https://httpbin.org/post";
const option3 = { method: "POST", body: "a=1" };
fetch(url3, option3)
  .then((res) => res.json())
  .then((json) => console.log(json));

const url4 = "https://httpbin.org/post";
const option4 = {
  method: "post",
  body: JSON.stringify({ a: 1 }),
  headers: { "Content-Type": "application/json" },
};
fetch(url4, option4)
  .then((res) => res.json())
  .then((json) => console.log(json));

const params5 = new URLSearchParams();
params5.append("a", 1);
const url5 = "https://httpbin.org/post";
const option5 = { method: "POST", body: params5 };
fetch("https://httpbin.org/post", {})
  .then((res) => res.json())
  .then((json) => console.log(json));

const url6 = "https://domain.invalid/";
fetch(url6).catch((err) => console.error(err));
```

---

## for es module

```bash
[linux:project ] $ vi package.json
{
    "type": "module"
}
```

```javascript
import fetch from "node-fetch";

const url1 = "https://github.com/";
(async function (url) {
  const response = await fetch(url);
  const body = await response.text();

  console.log(body);
})(url1);

async function jsonEx(url) {
  const response = await fetch(url);
  const json = await response.json();

  console.log(json);
}
const url2 = "https://api.github.com/users/github";
jsonEx(url2);

const simplePostEx = async function (url, option) {
  const response = await fetch(url, option);
  const json = await response.json();

  console.log(json);
};
const url3 = "https://httpbin.org/post";
const option3 = { method: "POST", body: "a=1" };
simplePostEx(url3, option3);

const url4 = "https://httpbin.org/post";
const option4 = {
  method: "post",
  body: JSON.stringify({ a: 1 }),
  headers: { "Content-Type": "application/json" },
};
const postWithJson = async function (url, option) {
  const response = await fetch(url, option);
  const json = await response.json();

  console.log(json);
};
postWithJson(url4, option4);

const params5 = new URLSearchParams();
params5.append("a", 1);
const url5 = "https://httpbin.org/post";
const option5 = { method: "POST", body: params5 };
const postWithFormParameters = async (url, option) => {
  const response = await fetch(url, option);
  const json = await response.json();

  console.log(json);
};
postWithFormParameters(url5, option5);

const url6 = "https://domain.invalid/";
const handlingExceptions = async (url) => {
  try {
    await fetch(url6);
  } catch (error) {
    console.log(error);
  }
};
handlingExceptions(url6);
```


---

## ref

[node-fetch](https://github.com/node-fetch/node-fetch)

