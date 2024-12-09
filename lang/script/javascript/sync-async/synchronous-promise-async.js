function begin(m) {
    console.log(`begin ${m}`);
    return Promise.resolve(m);
}

function sayHi(t) {
    return new Promise((resolve) => {
        setTimeout(() => {
            console.log(`hi (late ${t} sec)`);
            resolve(t);
        }, t * 1000);
    });
}

function finish(m) {
    console.log(`finish ${m}`);
    return Promise.resolve(m);
}

function main() {
    let t = 3;
    (async function (p) {
        await begin(p);
        await sayHi(p);
        await finish(p);
    })(t);
}

main();
