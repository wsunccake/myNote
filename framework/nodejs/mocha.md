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
// for common js
const {assert} = require('chai');

// for module
// import { assert } from 'chai';

// for module
// import * as _chai from "chai";
// const { assert } = _chai['default'];

describe('suite', () => {
    it('spec', () => {
        assert.equal(1 + 1, 2);
    })
});

[linux:project] $ npx mocha
[linux:project] $ npx mocha --file test/test.js
```


---

## hook

before/after, beforeEach, afterEach

```javascript
describe("top", function () {
    before(function () {
        console.log("top before");
    });
    after(function () {
        console.log("top after");
    });
    beforeEach(function () {
        console.log("top beforeEach");
    });
    afterEach(function () {
        console.log("top afterEach");
    });
    it("test1", function () {
        console.log("top test1");
    });
    describe("sublevel", function() {
        before(function () {
            console.log("sublevel before");
        });
        after(function () {
            console.log("sublevel after");
        });
        beforeEach(function () {
            console.log("sublevel beforeEach");
        });
        afterEach(function () {
            console.log("sublevel afterEach");
        });
        it("test1", function () {
            console.log("sublevel test1");
        });
        it("test2", function () {
            console.log("sublevel test2");
        });
    });
    it("test2", function () {
        console.log("top test2");
    });
});
```
