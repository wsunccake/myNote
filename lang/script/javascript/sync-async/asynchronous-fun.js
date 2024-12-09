function begin(m) {
    console.log(`begin ${m}`);
};

let sayHi = function (t) {
    setTimeout(() => {
        console.log(`hi (late ${t} sec)`);
    }, t * 1000);
}

let finish = (m) => {
    console.log(`finish ${m}`);
}

// asynchronous
function main() {
    let t = 3;
    begin(t);
    sayHi(t);
    finish(t);
}

main();