# jsx

```js
// index.js
const element = <h1>hello jsx</h1>;

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  element
);
```


## embedding expression

```js
// expression
function formatName(user) {
  return user.firstName + ' ' + user.lastName;
}
const user = {
  firstName: 'Harper',
  lastName: 'Perez'
};
const element = (
  <h1>
    Hello, {formatName(user)}!
  </h1>
);

// if
const x = 5;
let text = "Goodbye";
if (x < 10) {
  text = "Hello";
}
const element = <h1>{text}</h1>;

// ternary
const x = 5;
const element = <h1>{(x) < 10 ? "Hello" : "Goodbye"}</h1>;

// loop
const element = () => {
  let fruits = ["Apples", "Bananas"];
  let texts = [];
  for (const fruit of fruits) {
    texts.push(<li>{fruit}</li>);
  }
  return (
    <ul>
      {texts}
    </ul>
  );
};
```


---

## specifying attributes with jsx

```js
const element = <a href="https://www.reactjs.org"> link </a>;
const element = <img src={user.avatarUrl}></img>;
```


---

## specifying children with jsx

```js
const element = <img src={user.avatarUrl} />;
const element = (
  <div>
    <h1>Hello!</h1>
    <h2>Good to see you here.</h2>
  </div>
);
```


---

## jpx prevent injection attack

```js
const title = response.potentiallyMaliciousInput;
const element = <h1>{title}</h1>;
```


---

## jsx represent object

```js
const element = (
  <h1 className="greeting">
    Hello, world!
  </h1>
);

const element = React.createElement(
  'h1',
  {className: 'greeting'},
  'Hello, world!'
);

const element = {
  type: 'h1',
  props: {
    className: 'greeting',
    children: 'Hello, world!'
  }
};
```
