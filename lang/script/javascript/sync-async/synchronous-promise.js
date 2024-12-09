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
    begin(t)
        .then((res) => sayHi(res))
        .then((res) => finish(res))
        .catch((err) => console.error("error: ", err));
}

main();
