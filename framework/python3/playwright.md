# playwright

## install

```bash
linux:~ $ pip install playwright    # 1.49

# for user
linux:~ $ playwright install                            # all browser
linux:~ $ playwright install  [--with-deps] [chromium]  # chromium
# chromium, chromium-headless-shell, chromium-tip-of-tree-headless-shell,
# chrome, chrome-beta, msedge, msedge-beta, msedge-dev
# _bidiChromium, firefox, webkit
linux:~ $ playwright install  --list

# for system
linux:~ $ export PLAYWRIGHT_BROWSERS_PATH=/opt/playwright-browsers 
linux:~ $ sudo playwright install
linux:~ $ chmod -R 755 $PLAYWRIGHT_BROWSERS_PATH
```

## trace viewer

```python
from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    context.tracing.start(
        screenshots=True,
        snapshots=True
    )

    url = "https://www.example.com"
    page.goto(url)
    page.wait_for_load_state("networkidle")
    trace_file_path = "playwright_trace.zip"

    context.tracing.stop(path=trace_file_path)
    browser.close()
    print(f"Trace saved to {trace_file_path}")

with sync_playwright() as playwright:
    run(playwright)
```

```bash
linux:~ $ playwright show-trace playwright_trace.zip
```

## har / http archive

```python
from playwright.sync_api import sync_playwright

def run(playwright):
    har_file = "network_log.har"
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context(
        record_har_path=har_file
    )
    page = context.new_page()

    url = "https://www.example.com"
    page.goto(url)
    page.wait_for_load_state("networkidle")

    context.close()
    browser.close()
    print(f"HAR saved as {har_file}")

with sync_playwright() as playwright:
    run(playwright)
```

```python
from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    trace_file = "trace_events.zip"
    context.tracing.start(
        snapshots=True,
        screenshots=True
    )

    url = "https://www.example.com"
    page.goto(url)
    page.wait_for_load_state("networkidle")

    context.tracing.stop(path=trace_file)
    browser.close()
    print(f"Trace events saved to {trace_file}")

with sync_playwright() as playwright:
    run(playwright)
```

## performance

```python
import json
from playwright.sync_api import sync_playwright


def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    url = "https://www.example.com"
    page.goto(url)
    page.wait_for_load_state("networkidle")
    performance_metrics = page.evaluate(
        "() => JSON.stringify(window.performance.toJSON())"
    )
    performance_data = json.loads(performance_metrics)

    output_file = "performance_metrics.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(performance_data, f, indent=2)

    browser.close()
    print(f"Performance metrics saved to {output_file}")

with sync_playwright() as playwright:
    run(playwright)
```

## selenium grid

```bash
linux:~ $ SELENIUM_REMOTE_URL=http://<hub>:4444 python test.py
```
