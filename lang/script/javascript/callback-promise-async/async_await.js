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

async function getData(t) {
    // try {
    //     await fetchData(t).then((data) => { console.log("result: ", data); });
    // } catch (error) {
    //     await fetchData(t).catch((data) => { console.log("err: ", data); });
    // }
    // =>
    await fetchData(t).
        then((data) => { console.log("result: ", data); }).
        catch((data) => { console.log("err: ", data); });
}


function main() {
    let t = -1;
    getData(t);
}

main();