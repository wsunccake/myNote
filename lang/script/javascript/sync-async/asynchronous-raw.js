// asynchronous
function main() {
    let t = 3;
    console.log(`begin ${t}`);
    setTimeout(() => {
        console.log(`hi (late ${t} sec)`);
    }, t * 1000);
    console.log(`finish ${t}`);
}

main();