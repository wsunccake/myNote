# gulp 4

## install

```bash
[linux:project] $ npm install --global gulp-cli
[linux:project] $ npm install --save-dev gulp
[linux:project] $ `npm bin`/gulp --version
```


---

## test

```bash
[linux:project] $ vi gulpfile.js
function defaultTask(cb) {
  // default task
  cb();
}

exports.default = defaultTask

[linux:project] $ gulp --tasks
[linux:project] $ gulp
```


---

## task

### common js

```bash
[linux:project] $ vi gulpfile.js
const gulp = require('gulp');

function clean(cb) {
  // body omitted
  cb();
}

function build(cb) {
  // body omitted
  cb();
}

exports.build = build;
exports.default = series(clean, build);
```


### es module

```bash
[linux:project] $ npm install --save-dev @babel/core @babel/preset-env @babel/register
[linux:project] $ vi gulpfile.babel.js
import gulp from 'gulp';

function clean(cb) {
  // body omitted
  cb();
}

function build(cb) {
  // body omitted
  cb();
}

exports.build = build;
exports.default = gulp.series(clean, build);

[linux:project] $ vi 
{
  "presets": ["@babel/preset-env"]
}
```
