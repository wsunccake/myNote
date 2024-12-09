let fetchData = function (t, callback) {
    console.log("start to load...");
    setTimeout(() => {
        callback(null, t);
    }, t * 1000);
}

function main() {
    let t = 3;
    fetchData(t, (error, result) => {
        if (error) {
            console.error("error: ", error);
        } else {
            console.log("result: ", result);
        }
    });
}

main();