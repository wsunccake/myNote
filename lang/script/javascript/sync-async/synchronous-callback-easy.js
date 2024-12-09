function begin(m) {
    console.log(`begin ${m}`);
};

let sayHi = function (t, cb) {
    setTimeout(() => {
        console.log(`hi (late ${t} sec)`);
        cb(t);
    }, t * 1000);
}

let finish = (m) => {
    console.log(`finish ${m}`);
}

// synchronous
function main() {
    let t = 3;
    begin(t);
    sayHi(t, (m) => {
        console.log(`finish ${m}`);
    });
    // =>
    // sayHi(3, finish);
}

main();