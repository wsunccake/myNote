# gulp 4.x

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
};

const build = (cb) => {
  // body omitted
  cb();
};

exports.clean = clean;
exports.build = build;
exports.default = gulp.series(clean, build);
```


### es module

```bash
[linux:project] $ npm install --save-dev @babel/core @babel/preset-env @babel/register
[linux:project] $ vi .babelrc
{
  "presets": ["@babel/preset-env"]
}
[linux:project] $ vi gulpfile.babel.js
import gulp from 'gulp';

export function clean(cb) {
  // body omitted
  cb();
};

export const build = (cb) => {
  const e = util.promisify(exec);
  const r = async () => {
    const { stdout, stderr } = await e("echo build");
    console.log(`stdout: ${stdout}`);
    console.error(`stderr: ${stderr}`);
  };
  r();
 
  cb();
};

export const run = (cb) => {
  exec("echo run", (error, stdout, stderr) => {
    if (error) {
      console.error(`error: ${error}`);
    } else {
      console.log(`stdout: ${stdout}`);
      console.error(`stderr: ${stderr}`);
    };
  });
  cb();
};

export default gulp.series(clean, build);
```
