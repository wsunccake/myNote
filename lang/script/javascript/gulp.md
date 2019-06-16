# gulp


## hello

`project`

```bash
linux:~ # mkdir project
linux:~ # cd project
linux:~/project # npm install --save-dev gulp
linux:~/project # vi gulpfile.js
linux:~/project # mkdir src
linux:~/project # vi src/hello.js
```

`gulpfile.js`

```javascript
var gulp = require('gulp');
var exec = require('child_process').exec;

gulp.task('default', function() {
    console.log("gulp task");
    exec('node src/hello.js', function (error, stdout, stderr) {
        console.log(stdout);
    });
});
```

`src/hello.js`

```javascript
console.log('Hello JavaScript');
```

`run`

```bash
linux:~/project # gulp
```

