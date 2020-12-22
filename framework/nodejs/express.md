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

```javasript
app.get('/example/a', function (req, res) {
  res.send('Hello from A!')
})

app.get('/example/b', function (req, res, next) {
  console.log('the response will be sent by the next function ...')
  next()
}, function (req, res) {
  res.send('Hello from B!')
})

var cb0 = function (req, res, next) {
  console.log('CB0')
  next()
}

var cb1 = function (req, res, next) {
  console.log('CB1')
  next()
}

var cb2 = function (req, res) {
  res.send('Hello from C!')
}

app.get('/example/c', [cb0, cb1, cb2])

var cb0 = function (req, res, next) {
  console.log('CB0')
  next()
}

var cb1 = function (req, res, next) {
  console.log('CB1')
  next()
}

app.get('/example/d', [cb0, cb1], function (req, res, next) {
  console.log('the response will be sent by the next function ...')
  next()
}, function (req, res) {
  res.send('Hello from D!')
})
```


### response method

res.download(): Prompt a file to be downloaded.

res.end(): End the response process.

res.json(): Send a JSON response.

res.jsonp(): Send a JSON response with JSONP support.

res.redirect(): Redirect a request.

res.render(): Render a view template.

res.send(): Send a response of various types.

res.sendFile(): Send a file as an octet stream.

res.sendStatus(): Set the response status code and send its string representation as the response body.


### app.route

```javascript
app.route('/book')
  .get(function (req, res) {
    res.send('Get a random book')
  })
  .post(function (req, res) {
    res.send('Add a book')
  })
  .put(function (req, res) {
    res.send('Update the book')
  })
```


### express.Router

```javascript
// birds.js
var express = require('express')
var router = express.Router()

// middleware that is specific to this router
router.use(function timeLog (req, res, next) {
  console.log('Time: ', Date.now())
  next()
})
// define the home page route
router.get('/', function (req, res) {
  res.send('Birds home page')
})
// define the about route
router.get('/about', function (req, res) {
  res.send('About birds')
})

module.exports = router

// app.js
var birds = require('./birds')

// ...

app.use('/birds', birds)
```


---

## writing middleware

### middleware function myLogger

```javascript
var express = require('express')
var app = express()

var myLogger = function (req, res, next) {
  console.log('LOGGED')
  next()
}

app.use(myLogger)

app.get('/', function (req, res) {
  res.send('Hello World!')
})

app.listen(3000)
```


### middleware function requestTime

```javascript
var express = require('express')
var app = express()

var requestTime = function (req, res, next) {
  req.requestTime = Date.now()
  next()
}

app.use(requestTime)

app.get('/', function (req, res) {
  var responseText = 'Hello World!<br>'
  responseText += '<small>Requested at: ' + req.requestTime + '</small>'
  res.send(responseText)
})

app.listen(3000)
```


### middleware function validateCookies

```javascript
// cookieValidator.js
async function cookieValidator (cookies) {
  try {
    await externallyValidateCookie(cookies.testCookie)
  } catch {
    throw new Error('Invalid cookies')
  }
}

// app.js
var express = require('express')
var cookieParser = require('cookie-parser')
var cookieValidator = require('./cookieValidator')

var app = express()

async function validateCookies (req, res, next) {
  await cookieValidator(req.cookies)
  next()
}

app.use(cookieParser())

app.use(validateCookies)

// error handler
app.use(function (err, req, res, next) {
  res.status(400).send(err.message)
})

app.listen(3000)
```


### configurable middleware

```javascript
// my-middleware.js
module.exports = function (options) {
  return function (req, res, next) {
    // Implement the middleware function based on the options object
    next()
  }
}

// app.js
var mw = require('./my-middleware.js')

app.use(mw({ option1: '1', option2: '2' }))
```


---

## using middleware

### application-level middleware

```javascript
app.use(function (req, res, next) {
  console.log('Time:', Date.now())
  next()
})

app.use('/user/:id', function (req, res, next) {
  console.log('Request Type:', req.method)
  next()
})

app.get('/user/:id', function (req, res, next) {
  res.send('USER')
})
```

```javascript
app.use('/user/:id', function (req, res, next) {
  console.log('Request URL:', req.originalUrl)
  next()
}, function (req, res, next) {
  console.log('Request Type:', req.method)
  next()
})

app.get('/user/:id', function (req, res, next) {
  console.log('ID:', req.params.id)
  next()
}, function (req, res, next) {
  res.send('User Info')
})

// handler for the /user/:id path, which prints the user ID
app.get('/user/:id', function (req, res, next) {
  res.end(req.params.id)
})
```

```javascript
app.get('/user/:id', function (req, res, next) {
  // if the user ID is 0, skip to the next route
  if (req.params.id === '0') next('route')
  // otherwise pass the control to the next middleware function in this stack
  else next()
}, function (req, res, next) {
  // send a regular response
  res.send('regular')
})

// handler for the /user/:id path, which sends a special response
app.get('/user/:id', function (req, res, next) {
  res.send('special')
})
```

```javascript
function logOriginalUrl (req, res, next) {
  console.log('Request URL:', req.originalUrl)
  next()
}

function logMethod (req, res, next) {
  console.log('Request Type:', req.method)
  next()
}

var logStuff = [logOriginalUrl, logMethod]
app.get('/user/:id', logStuff, function (req, res, next) {
  res.send('User Info')
})
```


### router-level middleware

```javascript
var express = require('express')
var app = express()
var router = express.Router()

// a middleware function with no mount path. This code is executed for every request to the router
router.use(function (req, res, next) {
  console.log('Time:', Date.now())
  next()
})

// a middleware sub-stack shows request info for any type of HTTP request to the /user/:id path
router.use('/user/:id', function (req, res, next) {
  console.log('Request URL:', req.originalUrl)
  next()
}, function (req, res, next) {
  console.log('Request Type:', req.method)
  next()
})

// a middleware sub-stack that handles GET requests to the /user/:id path
router.get('/user/:id', function (req, res, next) {
  // if the user ID is 0, skip to the next router
  if (req.params.id === '0') next('route')
  // otherwise pass control to the next middleware function in this stack
  else next()
}, function (req, res, next) {
  // render a regular page
  res.render('regular')
})

// handler for the /user/:id path, which renders a special page
router.get('/user/:id', function (req, res, next) {
  console.log(req.params.id)
  res.render('special')
})

// mount the router on the app
app.use('/', router)
```

```javascript
var express = require('express')
var app = express()
var router = express.Router()

// predicate the router with a check and bail out when needed
router.use(function (req, res, next) {
  if (!req.headers['x-auth']) return next('router')
  next()
})

router.get('/user/:id', function (req, res) {
  res.send('hello, user!')
})

// use the router and 401 anything falling through
app.use('/admin', router, function (req, res) {
  res.sendStatus(401)
})
```


---

## overriding express api
