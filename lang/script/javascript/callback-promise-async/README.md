# callback, promise, async/await

```javascript
function f1() {
  return "Hello! ExplainThis!";
}
f1(); // 輸出: "Hello! ExplainThis!"

// async
async function f2() {
  return "Hello! ExplainThis!";
}
f2(); // 輸出: Promise {<fulfilled>: 'Hello! ExplainThis!'}

f2().then((result) => {
  console.log(result); // "Hello! ExplainThis!"
});

// promise
function f3() {
  return Promise.resolve("Hello! ExplainThis!");
}
f3(); // 輸出: Promise {<fulfilled>: 'Hello! ExplainThis!'}

f3().then((result) => {
  console.log(result); // "Hello! ExplainThis!"
});
```

- [callback](./callback.js)
- [promise](./promise.js)
- [async/await](./async_await.js)
