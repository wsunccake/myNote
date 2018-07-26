# React


## Hello

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8" />
    <title>Hello React!</title>
    <script crossorigin src="https://unpkg.com/react@16/umd/react.production.min.js"></script>
    <script crossorigin src="https://unpkg.com/react-dom@16/umd/react-dom.production.min.js"></script>
</head>
<body>
<div id="root"></div>
    <script>
        ReactDOM.render(React.createElement("h1", null, "Hello React"), document.getElementById('root'));
    </script>
</body>
</html>
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
const cl = React.createClass({displayName: "intg",
  render() {
    return React.createElement("ul", null,
      React.createElement("li", null, "React"),
      React.createElement("li", null, "AngularJS"),
      React.createElement("li", null, "Vue.JS"),
    )
  }
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
