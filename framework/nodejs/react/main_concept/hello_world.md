# hello world

## package

```bash
linux:~ $ npm install -g create-react-app
linux:~ $ create-react-app hello-world
linux:~ $ cd hello-world
```

---

## run

```bash
linux:~/hello-world $ npm start
linux:~/hello-world $ npm run build

linux:~ $ curl http://localhost:3000
```

---

## folder

```bash
linux:~/hello-world $ tree -L 1 hello-world
hello-world
├── node_modules
├── package.json
├── package-lock.json
├── public
├── README.md
└── src

3 directories, 3 files

linux:~/hello-world $ tree hello-world/src
hello-world/src
├── App.css
├── App.js
├── App.test.js
├── index.css
├── index.js
├── logo.svg
├── reportWebVitals.js
└── setupTests.js

0 directories, 8 files

linux:~/hello-world $ tree hello-world/public
hello-world/public
├── favicon.ico
├── index.html
├── logo192.png
├── logo512.png
├── manifest.json
└── robots.txt

0 directories, 6 files
```

---

## index.js

```bash
linux:~/hello-world $ vi hello-world/src/index.js
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
->
root.render(
    <h1> Hello world!</h1>
);
```
