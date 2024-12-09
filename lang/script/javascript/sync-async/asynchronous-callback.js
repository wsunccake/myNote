function begin(m, cb) {
    console.log(`begin ${m}`);
    cb(null, m);
};

let sayHi = function (t, cb) {
    setTimeout(() => {
        console.log(`hi (late ${t} sec)`);
        cb(null, t);
    }, t * 1000);
}

let finish = (m, cb) => {
    console.log(`finish ${m}`);
    cb(null, m);
}

// asynchronous
function main() {
    let t = 3;
    begin(t, (err, res) => { });
    sayHi(3, (err, res) => { });
    finish(t, (err, res) => { });
}

main();