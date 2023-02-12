# React

## Hello

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>React App</title>
    <script
      crossorigin
      src="https://unpkg.com/react@18/umd/react.development.js"
    ></script>
    <script
      crossorigin
      src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"
    ></script>
    <script src="https://unpkg.com/babel-standalone@6/babel.min.js"></script>
  </head>

  <body>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>
  </body>
  <script type="text/babel" src="index.js"></script>
</html>
```

```js
const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<h1>hello</h1>);
```

---

## React Element

`element`

```javascript
React.createElement("h1", null, "Hello React");
->
<h1>Hello React</h1>
```

```javascript
React.createElement("h1", {id: "t1", 'data-type': "title"}, "Hello React");
->
<h1 id="t1" data-type="title">Hello React</h1>
```

`child element`

```javascript
React.createElement(
  "ul",
  null,
  React.createElement("li", null, "React"),
  React.createElement("li", null, "AngularJS"),
  React.createElement("li", null, "Vue.JS")
);

->

var items = ["React", "AngularJS", "Vue.JS"];
var el = React.createElement("ul", null, items.map( i =>
  React.createElement("li", null, i)
));
```

---

## React Component

`createClass`

在 15 之前才有支援, 16 之後不支援

```javascript
const cl = React.createClass({
  displayName: "intg",
  render() {
    return React.createElement(
      "ul",
      null,
      React.createElement("li", null, "React"),
      React.createElement("li", null, "AngularJS"),
      React.createElement("li", null, "Vue.JS")
    );
  },
});

ReactDOM.render(
  React.createElement(cl, null, null),
  document.getElementById("root")
);
```

`createComponent`

`ES6 class`

---

## Reference

[React](https://doc.react-china.org/)
