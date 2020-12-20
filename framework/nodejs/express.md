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


---

## basic routing

```javascript
// app.METHOD(PATH, HANDLER)
// app is an instance of express.
// METHOD is an HTTP request method, in lowercase.
// PATH is a path on the server.
// HANDLER is the function executed when the route is matched.

app.get('/', function (req, res) {
  res.send('Hello World!')
})

app.post('/', function (req, res) {
  res.send('Got a POST request')
})

app.put('/user', function (req, res) {
  res.send('Got a PUT request at /user')
})

app.delete('/user', function (req, res) {
  res.send('Got a DELETE request at /user')
})
```


---

## static file

```javascript
// express.statc(root, [options])

app.use(express.static('public'))
app.use(express.static('files'))
app.use('/static', express.static('public'))
app.use('/static', express.static(path.join(__dirname, 'public')))
```


---

## routing

### route method

```javascript
var express = require('express')
var app = express()

// GET method route
app.get('/', function (req, res) {
  res.send('GET request to the homepage')
})

// POST method route
app.post('/', function (req, res) {
  res.send('POST request to the homepage')
})

app.all('/secret', function (req, res, next) {
  console.log('Accessing the secret section ...')
  next() // pass control to the next handler
})
```


### route path

```javascript
app.get('/', function (req, res) {
  res.send('root')
})

app.get('/about', function (req, res) {
  res.send('about')
})

app.get('/random.text', function (req, res) {
  res.send('random.text')
})

app.get('/ab?cd', function (req, res) {
  res.send('ab?cd')
})

app.get('/ab+cd', function (req, res) {
  res.send('ab+cd')
})

app.get('/ab*cd', function (req, res) {
  res.send('ab*cd')
})

app.get('/ab(cd)?e', function (req, res) {
  res.send('ab(cd)?e')
})

app.get(/a/, function (req, res) {
  res.send('/a/')
})

app.get(/.*fly$/, function (req, res) {
  res.send('/.*fly$/')
})
```


### route parameter

```javascript
app.get('/users/:userId/books/:bookId', function (req, res) {
  res.send(req.params)
})
```


### route handler

```javascript
```

