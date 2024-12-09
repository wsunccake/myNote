function begin(m) {
    console.log(`begin ${m}`);
};

let finish = (m) => {
    console.log(`finish ${m}`);
}

let sayHi = function (t) {
    setTimeout(() => {
        console.log(`hi (late ${t} sec)`);
        finish(t);
    }, t * 1000);
}

// synchronous
function main() {
    let t = 3;
    begin(t);
    sayHi(t);
}

main();