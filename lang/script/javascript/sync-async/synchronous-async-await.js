async function begin(m) {
    console.log(`begin ${m}`);
}

function sayHi(t) {
    return new Promise((resolve) => {
        setTimeout(() => {
            console.log(`hi (late ${t} sec)`);
            resolve(t);
        }, t * 1000);
    });
}

async function finish(m) {
    console.log(`finish ${m}`);
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
