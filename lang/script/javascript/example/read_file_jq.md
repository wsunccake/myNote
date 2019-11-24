## read file

```bash
linux:~/project # tree
.
├── ex.js
├── index.html
├── q1.csv
└── q2.csv
```

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <script
            src="https://code.jquery.com/jquery-3.4.1.min.js"
            integrity="sha256-CSXorXvZcTkaix6Yvo6HppcZGetbYMGWSFlBw8HfCJo="
            crossorigin="anonymous"></script>

    <script type="text/javascript" src="ex.js"></script>

</head>
<body>

</body>
</html>
```


### example1

```javascript
let dataArray = [];
let getCSVData = function (csvFile) {
    console.log(csvFile);
    let tmpArray = [];

    $.get(csvFile, function (csv) {
        let content_lines = csv.split("\n");
        for (let i in content_lines) {
            let lines = content_lines[i].split(",");
            console.log('get: ', lines);
            tmpArray.push([lines[0], parseFloat(lines[1])]);
        }
        dataArray.push(tmpArray);
    });
};

getCSVData('q1.csv');
console.log('final: ', dataArray);
// undefined
console.log('final dataArray[0]: ', dataArray[0]);

```


### example2

```javascript
let dataArray = [];
let getCSVData = function (csvFile) {
    console.log(csvFile);
    let tmpArray = [];

    $.get(csvFile, function (csv) {
        let content_lines = csv.split("\n");
        for (let i in content_lines) {
            let lines = content_lines[i].split(",");
            console.log('get: ', lines);
            tmpArray.push([lines[0], parseFloat(lines[1])]);
        }
        dataArray.push(tmpArray);
    });
};

let q1 = getCSVData('q1.csv');

$.when(q1).done(function () {
    console.log("when q1: ", q1);
    console.log('final: ', dataArray);
    // undefined
    console.log('final dataArray[0]: ', dataArray[0]);
});
```


### example3

```javascript
let dataArray = [];
let getData = $.get('q1.csv', function (csv) {
    let tmpArray = [];
    let content_lines = csv.split("\n");

    for (let i in content_lines) {
        let lines = content_lines[i].split(",");
        console.log('get: ', lines);
        tmpArray.push([lines[0], parseFloat(lines[1])]);
    }
    dataArray.push(tmpArray);
});

$.when(getData).done(function () {
    console.log("final: ", dataArray);
    // defined
    console.log('final dataArray[0]: ', dataArray[0]);
});
```


### example4

```javascript
let dataArray = [];
let getData = function(csvFile) {
    console.log(csvFile);
    let csvData = $.get(csvFile, function(csv) {
        let tmpArray = [];
        let content_lines = csv.split("\n");
        for (let i in content_lines) {
           let lines = content_lines[i].split(",");
           console.log('get: ', lines);
           tmpArray.push([lines[0], parseFloat(lines[1])]);
        }
        dataArray.push(tmpArray);
    });

    $.when(csvData).done(function(x) {
       console.log(csvFile, "get data: ", dataArray);
    });
};

$.when(getData('q1.csv'), getData('q2.csv')).done(function() {
    console.log('final: ', dataArray);
    // undefined
    console.log('final dataArray[0]: ', dataArray[0]);
});
```


### example5

```javascript
let dataArray = [];
let getData = function(csvFile) {
    console.log(csvFile);
    return new Promise(function(resolve, reject) {
        let tmpArray = [];
        $.get(csvFile, function(csv) {
            let content_lines = csv.split("\n");
            for (let i in content_lines) {
                let lines = content_lines[i].split(",");
                console.log('get: ', lines);
                tmpArray.push([lines[0], parseFloat(lines[1])]);
            }
            dataArray.push(tmpArray);
            console.log(csvFile, "get data: ", dataArray);
            resolve(tmpArray);
        });
    });
};

async function getAllData() {
   await getData('q1.csv');
   await getData('q2.csv');
    console.log('final: ', dataArray);
    // defined
    console.log('final dataArray[0]: ', dataArray[0]);
}

getAllData();
```
