// synchronous
function main() {
    let t = 3;
    console.log(`begin ${t}`);
    setTimeout(() => {
        console.log(`hi (late ${t} sec)`);
        console.log(`finish ${t}`);
    }, t * 1000);
}

main();