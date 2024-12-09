let fetchData = function (t) {
    return new Promise((resolve, reject) => {
        console.log("start to load...");
        setTimeout(() => {
            if (t > 0) {
                resolve(t);
            } else {
                reject(t);
            }
        }, t * 1000);
    });
}

function main() {
    let t = 3;
    fetchData(t)
        .then((result) => {
            console.log("result: ", result);
        })
        .catch((error) => {
            console.error("error: ", error);
        });
}

main();