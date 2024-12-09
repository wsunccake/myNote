# lighthouse

---

## content

- [install](#install)
- [test](#test)
- [example](#example)
  - [chrome-launcher](#chrome-launcher)
  - [puppeteer](#puppeteer)
  - [user flow](#user-flow)
- [viewer](#viewer)
- [ref](#ref)

---

## install

```bash
linux:~ $ npm install -g lighthouse
```

---

## test

```bash
linux:~ $ lighthouse https://www.google.com
```

---

## example

### chrome-launcher

```javascript
// app.js
import { launch } from "chrome-launcher";
import lighthouse from "lighthouse";
import fs from "fs";

(async () => {
  const chrome = await launch({ chromeFlags: ["--headless"] });
  //  const options = { logLevel: 'info', output: 'html', onlyCategories: ['performance'], port: chrome.port };
  const options = { logLevel: "info", output: "html", port: chrome.port };
  const runnerResult = await lighthouse("https://www.google.com", options);

  console.log("Report is done for", runnerResult.lhr.finalUrl);
  console.log(
    "Performance score was",
    runnerResult.lhr.categories.performance.score * 100
  );

  fs.writeFileSync("report.html", runnerResult.report, "utf-8");
  const jsonReport = JSON.stringify(runnerResult.lhr, null, 2);
  fs.writeFileSync("report.json", jsonReport, "utf-8");
  console.log("Reports saved as report.html and report.json");

  await chrome.kill();
})();
```

```bash
linux:~/demo $ npm install chrome-launcher lighthouse
linux:~/demo $ node app.js
```

### puppeteer

```javascript
// app.js
import puppeteer from "puppeteer";
import lighthouse from "lighthouse";
import fs from "fs";

(async () => {
  const browser = await puppeteer.launch({
    headless: true,
    args: ["--remote-debugging-port=9222"],
  });

  try {
    const options = {
      logLevel: "info",
      output: "html",
      port: 9222,
      formFactor: "desktop",
      screenEmulation: {
        disabled: false,
        width: 1920,
        height: 1080,
        deviceScaleFactor: 1,
        mobile: false,
      },
    };

    const urlToTest = "https://www.google.com";
    const runnerResult = await lighthouse(urlToTest, options);

    console.log("Report is done for", runnerResult.lhr.finalUrl);
    console.log(
      "Performance score was",
      runnerResult.lhr.categories.performance.score * 100
    );

    console.log("Lighthouse Scores:");
    for (const [category, data] of Object.entries(
      runnerResult.lhr.categories
    )) {
      console.log(`${category.toUpperCase()}: ${data.score * 100}`);
    }

    fs.writeFileSync("report.html", runnerResult.report, "utf-8");
    const jsonReport = JSON.stringify(runnerResult.lhr, null, 2);
    fs.writeFileSync("report.json", jsonReport, "utf-8");

    console.log("Reports saved as report.html and report.json");
  } catch (error) {
    console.error("Error running Lighthouse:", error);
  } finally {
    await browser.close();
  }
})();
```

```bash
linux:~/demo $ npm install puppeteer lighthouse
linux:~/demo $ node app.js
```

### user flow

```javascript
// app.js
import puppeteer from "puppeteer";
import { startFlow, desktopConfig } from "lighthouse";
import { writeFileSync } from "fs";

async function captureReport() {
  const browser = await puppeteer.launch({
    headless: false,
    args: ["--remote-debugging-port=9222", "--window-size=1920,1080"],
  });
  const page = await browser.newPage();
  desktopConfig.settings.screenEmulation = {
    disabled: false,
    width: 1920,
    height: 1080,
    deviceScaleFactor: 1,
    mobile: false,
  };

  const flow = await startFlow(page, { config: desktopConfig });
  const url = "https://web.dev/";

  // Phase 1 - Navigate
  await flow.navigate(url, { name: "navigate" });
  // await page.waitForNetworkIdle(5000);

  // Phase 2 - Interact
  await flow.startTimespan({ name: "interact" });

  await page.click("button[search-open]", { delay: 100 });
  const searchBox = await page.waitForSelector(
    "devsite-search[search-active] input"
  );
  await searchBox.type("CLS");
  await searchBox.press("Enter");
  const link = await page.waitForSelector(
    'devsite-content a[href="https://web.dev/articles/cls"]'
  );

  await flow.endTimespan();

  // Phase 3 - Analyze
  await flow.snapshot({ name: "snapshot" });

  // Phase 4 - Navigate
  await flow.navigate(async () => {
    await link.click();
  });

  await browser.close();

  const reportPath = "user-flow";
  writeFileSync(`${reportPath}.html`, await flow.generateReport());
  writeFileSync(
    `${reportPath}.json`,
    JSON.stringify(await flow.createFlowResult(), null, 2)
  );
}

captureReport();
```

---

## viewer

- [Lighthouse Report Viewer](https://googlechrome.github.io/lighthouse/viewer/)
- [Lighthouse Report Diff Tool](https://googlechrome.github.io/lighthouse-ci/difftool/)

---

## ref

- [lighthouse](https://github.com/GoogleChrome/lighthouse/)
