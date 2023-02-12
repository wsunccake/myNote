# class base component

## fetch api

```js
// App.js
import React from "react";

class App extends React.Component {
  constructor() {
    super();
    this.state = {
      fetchApiData: "",
      getApiData: "",
    };
  }

  componentDidMount() {
    fetch("https://api.covid19api.com/summary")
      .then((respo) => {
        return respo.json();
      })
      .then((data) => {
        let list = data.Global.NewConfirmed;
        this.setState({ fetchApiData: list });
      });
  }
  fetchData() {
    this.setState({ getApiData: this.state.fetchApiData });
  }

  render() {
    return (
      <>
        <h1 style={{ textAlign: "center" }}>Corona Cases</h1>
        <p>NewConfirmed : {this.state.getApiData}</p>
        <button onClick={() => this.fetchData()}>Fetch</button>
      </>
    );
  }
}

export default App;
```
