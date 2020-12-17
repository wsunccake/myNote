# express


## hello

```bash
[linux:~] $ mkdir myapp
[linux:~] $ cd myapp
[linux:myapp] $ npm init
[linux:myapp] $ npm install express
[linux:myapp] $ vi app.js
const express = require('express')
const app = express()
const port = 3000

app.get('/', (req, res) => {
  res.send('hello express!')
})

app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`)
})

[linux:myapp] $ node app.js

[linux:~] $ http://localhost:3000
```


---

## express application generator

```bash
[linux:~] $ npx express-generator --view=pug myapp
[linux:~] $ cd myapp
[linux:myapp] $ npm install
[linux:myapp] $ DEBUG=myapp:* npm start

[linux:~] $ http://localhost:3000
```
