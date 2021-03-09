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

```javascript
app.response.sendStatus = function (statusCode, type, message) {
  // code is intentionally kept simple for demonstration purpose
  return this.contentType(type)
    .status(statusCode)
    .send(message)
}
```

```javascript
res.sendStatus(404, 'application/json', '{"error":"resource not found"}')
```


---

## using template engine

```bash
[linux:myapp] $ npm install pug --save

[linux:myapp] $ vi views/index.pug
html
  head
    title= title
  body
    h1= message

[linux:myapp] $ vi app.js
app.set('view engine', 'pug')
...
app.get('/', function (req, res) {
  res.render('index', { title: 'Hey', message: 'Hello there!' })
})
```


---

## error handling

### catching Error

```javascript
app.get('/', function (req, res) {
  throw new Error('BROKEN') // Express will catch this on its own.
})
```

```javascript
app.get('/', function (req, res, next) {
  fs.readFile('/file-does-not-exist', function (err, data) {
    if (err) {
      next(err) // Pass errors to Express.
    } else {
      res.send(data)
    }
  })
})
```

```javascript
app.get('/user/:id', async function (req, res, next) {
  var user = await getUserById(req.params.id)
  res.send(user)
})
```

```javascript
app.get('/', [
  function (req, res, next) {
    fs.writeFile('/inaccessible-path', 'data', next)
  },
  function (req, res) {
    res.send('OK')
  }
])
```

```javascript
app.get('/', function (req, res, next) {
  setTimeout(function () {
    try {
      throw new Error('BROKEN')
    } catch (err) {
      next(err)
    }
  }, 100)
})
```

```javascript
app.get('/', function (req, res, next) {
  Promise.resolve().then(function () {
    throw new Error('BROKEN')
  }).catch(next) // Errors will be passed to Express.
})
```

```javascript
app.get('/', [
  function (req, res, next) {
    fs.readFile('/maybe-valid-file', 'utf-8', function (err, data) {
      res.locals.data = data
      next(err)
    })
  },
  function (req, res) {
    res.locals.data = res.locals.data.split(',')[1]
    res.send(res.locals.data)
  }
])
```


### default error handler

```javascript
function errorHandler (err, req, res, next) {
  if (res.headersSent) {
    return next(err)
  }
  res.status(500)
  res.render('error', { error: err })
}
```


### writing error handler

```javascript
app.use(function (err, req, res, next) {
  console.error(err.stack)
  res.status(500).send('Something broke!')
})
```

```javascript
var bodyParser = require('body-parser')
var methodOverride = require('method-override')

app.use(bodyParser.urlencoded({
  extended: true
}))
app.use(bodyParser.json())
app.use(methodOverride())
app.use(logErrors)
app.use(clientErrorHandler)
app.use(errorHandler)

function logErrors (err, req, res, next) {
  console.error(err.stack)
  next(err)
}

function clientErrorHandler (err, req, res, next) {
  if (req.xhr) {
    res.status(500).send({ error: 'Something failed!' })
  } else {
    next(err)
  }
}

function errorHandler (err, req, res, next) {
  res.status(500)
  res.render('error', { error: err })
}
```

```javascript
app.get('/a_route_behind_paywall',
  function checkIfPaidSubscriber (req, res, next) {
    if (!req.user.hasPaid) {
      // continue handling this request
      next('route')
    } else {
      next()
    }
  }, function getPaidContent (req, res, next) {
    PaidContent.find(function (err, doc) {
      if (err) return next(err)
      res.json(doc)
    })
  })
```


---

## debugging

```bash
[linux:myapp] $ DEBUG=express:* node index.js
[linux:myapp] $ DEBUG=express:* node ./bin/www   # npx express-generator
```


---

## database integration

### cassandra

```bash
[linux:myapp] $ npm install cassandra-driver
```

```javascript
var cassandra = require('cassandra-driver')
var client = new cassandra.Client({ contactPoints: ['localhost'] })

client.execute('select key from system.local', function (err, result) {
  if (err) throw err
  console.log(result.rows[0])
})
```


### couchnode

```bash
[linux:myapp] $ npm install couchnode
```

```javascript
var couchbase = require('couchbase')
var bucket = (new couchbase.Cluster('http://localhost:8091')).openBucket('bucketName')

// add a document to a bucket
bucket.insert('document-key', { name: 'Matt', shoeSize: 13 }, function (err, result) {
  if (err) {
    console.log(err)
  } else {
    console.log(result)
  }
})

// get all documents with shoe size 13
var n1ql = 'SELECT d.* FROM `bucketName` d WHERE shoeSize = $1'
var query = N1qlQuery.fromString(n1ql)
bucket.query(query, [13], function (err, result) {
  if (err) {
    console.log(err)
  } else {
    console.log(result)
  }
})
```


### couchdb

```bash
[linux:myapp] $ npm install nano
```

```javascript
var nano = require('nano')('http://localhost:5984')
nano.db.create('books')
var books = nano.db.use('books')

// Insert a book document in the books database
books.insert({ name: 'The Art of war' }, null, function (err, body) {
  if (err) {
    console.log(err)
  } else {
    console.log(body)
  }
})

// Get a list of all books
books.list(function (err, body) {
  if (err) {
    console.log(err)
  } else {
    console.log(body.rows)
  }
})
```


### leveldb

```bash
[linux:myapp] $ npm install level levelup leveldown
```

```javascript
var levelup = require('levelup')
var db = levelup('./mydb')

db.put('name', 'LevelUP', function (err) {
  if (err) return console.log('Ooops!', err)

  db.get('name', function (err, value) {
    if (err) return console.log('Ooops!', err)

    console.log('name=' + value)
  })
})
```


### mysql

```bash
[linux:myapp] $ npm install mysql
```

```javascript
var mysql = require('mysql')
var connection = mysql.createConnection({
  host: 'localhost',
  user: 'dbuser',
  password: 's3kreee7',
  database: 'my_db'
})

connection.connect()

connection.query('SELECT 1 + 1 AS solution', function (err, rows, fields) {
  if (err) throw err

  console.log('The solution is: ', rows[0].solution)
})

connection.end()
```


### mongodb

```bash
[linux:myapp] $ npm install mongodb
```

```javascript
// for v2.*
var MongoClient = require('mongodb').MongoClient

MongoClient.connect('mongodb://localhost:27017/animals', function (err, db) {
  if (err) throw err

  db.collection('mammals').find().toArray(function (err, result) {
    if (err) throw err

    console.log(result)
  })
})
```

```javascript
// for v3.*
var MongoClient = require('mongodb').MongoClient

MongoClient.connect('mongodb://localhost:27017/animals', function (err, client) {
  if (err) throw err

  var db = client.db('animals')

  db.collection('mammals').find().toArray(function (err, result) {
    if (err) throw err

    console.log(result)
  })
})
```


### neo4j

```bash
[linux:myapp] $ npm install apoc
```

```javascript
var apoc = require('apoc')

apoc.query('match (n) return n').exec().then(
  function (response) {
    console.log(response)
  },
  function (fail) {
    console.log(fail)
  }
)
```


### oracle

```bash
[linux:myapp] $ npm install oracledb
```

```javascript
const oracledb = require('oracledb')
const config = {
  user: '<your db user>',
  password: '<your db password>',
  connectString: 'localhost:1521/orcl'
}

async function getEmployee (empId) {
  let conn

  try {
    conn = await oracledb.getConnection(config)

    const result = await conn.execute(
      'select * from employees where employee_id = :id',
      [empId]
    )

    console.log(result.rows[0])
  } catch (err) {
    console.log('Ouch!', err)
  } finally {
    if (conn) { // conn assignment worked, need to close
      await conn.close()
    }
  }
}

getEmployee(101)
```


### postgresql

```bash
[linux:myapp] $ npm install pg-promise
```

```javascript
var pgp = require('pg-promise')(/* options */)
var db = pgp('postgres://username:password@host:port/database')

db.one('SELECT $1 AS value', 123)
  .then(function (data) {
    console.log('DATA:', data.value)
  })
  .catch(function (error) {
    console.log('ERROR:', error)
  })
```


### redis

```bash
[linux:myapp] $ npm install redis
```

```javascript
var redis = require('redis')
var client = redis.createClient()

client.on('error', function (err) {
  console.log('Error ' + err)
})

client.set('string key', 'string val', redis.print)
client.hset('hash key', 'hashtest 1', 'some value', redis.print)
client.hset(['hash key', 'hashtest 2', 'some other value'], redis.print)

client.hkeys('hash key', function (err, replies) {
  console.log(replies.length + ' replies:')

  replies.forEach(function (reply, i) {
    console.log('    ' + i + ': ' + reply)
  })

  client.quit()
})
```


### sql server

```bash
[linux:myapp] $ npm install tedious
```

```javascript
var Connection = require('tedious').Connection
var Request = require('tedious').Request

var config = {
  server: 'localhost',
  authentication: {
    type: 'default',
    options: {
      userName: 'your_username', // update me
      password: 'your_password' // update me
    }
  }
}

var connection = new Connection(config)

connection.on('connect', function (err) {
  if (err) {
    console.log(err)
  } else {
    executeStatement()
  }
})

function executeStatement () {
  request = new Request("select 123, 'hello world'", function (err, rowCount) {
    if (err) {
      console.log(err)
    } else {
      console.log(rowCount + ' rows')
    }
    connection.close()
  })

  request.on('row', function (columns) {
    columns.forEach(function (column) {
      if (column.value === null) {
        console.log('NULL')
      } else {
        console.log(column.value)
      }
    })
  })

  connection.execSql(request)
}
```


### sqlite

```bash
[linux:myapp] $ npm install sqlite3
```

```javascript
var sqlite3 = require('sqlite3').verbose()
var db = new sqlite3.Database(':memory:')

db.serialize(function () {
  db.run('CREATE TABLE lorem (info TEXT)')
  var stmt = db.prepare('INSERT INTO lorem VALUES (?)')

  for (var i = 0; i < 10; i++) {
    stmt.run('Ipsum ' + i)
  }

  stmt.finalize()

  db.each('SELECT rowid AS id, info FROM lorem', function (err, row) {
    console.log(row.id + ': ' + row.info)
  })
})

db.close()
```


### elasticsearch

```bash
[linux:myapp] $ npm install elasticsearch
```

```javascript
```

###

```bash
[linux:myapp] $ npm install
```

```javascript
var elasticsearch = require('elasticsearch')
var client = elasticsearch.Client({
  host: 'localhost:9200'
})

client.search({
  index: 'books',
  type: 'book',
  body: {
    query: {
      multi_match: {
        query: 'express js',
        fields: ['title', 'description']
      }
    }
  }
}).then(function (response) {
  var hits = response.hits.hits
}, function (error) {
  console.trace(error.message)
})
```
