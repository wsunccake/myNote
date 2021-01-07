# mocha

## test

```bash
[linux:~] $ mkdir project
[linux:~] $ cd project

[linux:project] $ npm init
[linux:project] $ npm install --save-dev mocha
[linux:project] $ npm install --save-dev chai

[linux:project] $ mkdir test
[linux:project] $ vi test/test.js
const {assert} = require('chai');

describe('test', () => {
    it('1 + 1 == 2', () => {
        assert.equal(1 + 1, 2);
    })
});

[linux:project] $ npx mocha
[linux:project] $ npx mocha --file test/test.js
```
