# state and lifecycle

## converting function to class

```js
// index.js
const root = ReactDOM.createRoot(document.getElementById('root'));

function tick() {
  const element = (
    <div>
      <h1>Hello, world!</h1>
      <h2>It is {new Date().toLocaleTimeString()}.</h2>
    </div>
  );
  root.render(element);
}

setInterval(tick, 1000);
```

->

function component

```js
const root = ReactDOM.createRoot(document.getElementById('root'));

function Clock(props) {
  return (
    <div>
      <h1>Hello, world!</h1>
      <h2>It is {props.date.toLocaleTimeString()}.</h2>
    </div>
  );
}

function tick() {
  root.render(<Clock date={new Date()} />);
}

setInterval(tick, 1000);
```

->

class component

```js
const root = ReactDOM.createRoot(document.getElementById('root'));

class Clock extends React.Component {
  constructor(props) {
    super(props);
    this.state = {date: new Date()};
  }

  render() {
    return (
      <div>
        <h1>Hello, world!</h1>
        <h2>It is {this.state.date.toLocaleTimeString()}.</h2>
      </div>
    );
  }
}

function tick() {
  root.render(<Clock />);
}

setInterval(tick, 1000);
```


---

## adding lifecycle methods to class

```js
// index.js
class Clock extends React.Component {
  constructor(props) {
    super(props);
    // this.state.comment = 'Hello';        // wrong, not re-render a component
    this.state = {date: new Date()};        // correct
  }

  componentDidMount() {                     // lifecycle
    this.timerID = setInterval(
      () => this.tick(),
      1000
    );
  }

  componentWillUnmount() {                  // lifecycle
    clearInterval(this.timerID);
  }

  tick() {
    this.setState({
      date: new Date()
    });

    // wrong, state update may be asynchronous
    // this.setState({
    //   counter: this.state.counter + this.props.increment,
    // });

    // correct
    // this.setState((state, props) => ({
    // counter: state.counter + props.increment
    // }));

    // correct
    // this.setState(function(state, props) {
    // return {
    //     counter: state.counter + props.increment
    // };
    // });
  }

  render() {
    return (
      <div>
        <h1>Hello, world!</h1>
        <h2>It is {this.state.date.toLocaleTimeString()}.</h2>
      </div>
    );
  }
}

```