# selenium 4

---

## content

- [prerequisite](#prerequisite)
  - [chrome](#chrome)
  - [web driver](#web-driver)
  - [selenium server](#selenium-server)
  - [package](#package)
  - [test](#test)
- [locating element](#locating-element)
- [wait](#wait)
  - [explicit wait](#explicit-wait)
  - [implict wait](#implict-wait)
- [page object model](#page-object-model)
- [code generator](#code-generator)
  - [selenium ide](#selenium-ide)
  - [katalon recorder](#katalon-recorder)
- [HAR](#HAR)
  - [mitmproxy](#mitmproxy)
  - [cdp](#cdp)
- [ref](#ref)

---

## prerequisite

### chrome

```bash
linux:~ # curl -LO https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
linux:~ # dpkg -i google-chrome-stable_current_amd64.deb

linux:~ # google-chrome --version
linux:~ # google-chrome-stable --version
```

### web driver

- [chrome](https://sites.google.com/chromium.org/driver/)
- [firefox](https://github.com/mozilla/geckodriver/releases)
- [safari](https://webkit.org/blog/6900/webdriver-support-in-safari-10/)
- [edge](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/?form=MA13LH)

```bash
linux:~ # curl -LO https://storage.googleapis.com/chrome-for-testing-public/126.0.6478.126/linux64/chromedriver-linux64.zip
linux:~ # unzip chromedriver-linux64.zip -d /usr/local/
linux:~ # ln -s /usr/local/chromedriver-linux64/chromedriver /usr/local/bin/.

linux:~ # chromedriver --version
```

### selenium server

- [SeleniumHQ / selenium](https://github.com/SeleniumHQ/selenium/releases/)

```bash
linux:~ # curl -LO https://github.com/SeleniumHQ/selenium/releases/download/selenium-4.22.0/selenium-server-4.22.0.jar

linux:~ # java -jar ./selenium-server-4.22.0.jar --help
linux:~ # java -jar ./selenium-server-4.22.0.jar standalone --help
linux:~ # java -jar ./selenium-server-4.22.0.jar standalone [--host 0.0.0.0] [--port 4444]

# crash-dumps-dir
linux:~ # curl http://127.0.0.1:4444/ui/
```

### package

```bash
linux:~ # python3 --version
linux:~ # pip install selenium==4.22.0
```

### test

```python
# local example
from selenium import webdriver
from selenium.webdriver.common.by import By

web_url = "https://www.selenium.dev/selenium/web/web-form.html"
driver = webdriver.Chrome()

driver.get(web_url)
driver.save_screenshot('screen1.png')

title = driver.title
driver.implicitly_wait(0.5)

text_box = driver.find_element(by=By.NAME, value="my-text")
submit_button = driver.find_element(by=By.CSS_SELECTOR, value="button")

text_box.send_keys("Selenium")
submit_button.click()
driver.save_screenshot('screen2.png')

message = driver.find_element(by=By.ID, value="message")
text = message.text

driver.quit()
```

```python
# remote example
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

server_host = "127.0.0.1"
server_port = 4444

chrome_options = webdriver.ChromeOptions()

# DevToolsActivePort file doesn't exist
chrome_options.add_argument("--no-sandbox")

# default crash dir /tmp/Crashpad
chrome_options.add_argument(
    f"--crash-dumps-dir={os.path.expanduser('~/tmp/Crashpad')}")

chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Remote(
   command_executor=f'http://{server_host}:{server_port}/wd/hub',
   options=chrome_options)

web_url = "https://www.selenium.dev/selenium/web/web-form.html"

driver.set_window_size(1024, 768)
driver.get(web_url)
driver.save_screenshot('screen1.png')

title = driver.title
driver.implicitly_wait(0.5)

try:
    text_box = driver.find_element(by=By.NAME, value="notext")
    print(text_box.id)
except NoSuchElementException as e:
    print("no found element")
    print(e.msg)

text_box = driver.find_element(by=By.NAME, value="my-text")
submit_button = driver.find_element(by=By.CSS_SELECTOR, value="button")

text_box.send_keys("Selenium")
submit_button.click()
driver.save_screenshot('screen2.png')

message = driver.find_element(by=By.ID, value="message")
text = message.text

driver.quit()
```

- [List of Chromium Command Line Switches](https://peter.sh/experiments/chromium-command-line-switches/)

---

## locating element

```python
# before selenium 3.x
# deprecated
# element
driver.find_element_by_class_name("className")
driver.find_element_by_css_selector(".className")
driver.find_element_by_id("elementId")
driver.find_element_by_link_text("linkText")
driver.find_element_by_name("elementName")
driver.find_element_by_partial_link_text("partialText")
driver.find_element_by_tag_name("elementTagName")
driver.find_element_by_xpath("xpath")

# elements
driver.find_elements_by_class_name("className")
driver.find_elements_by_css_selector(".className")
driver.find_elements_by_id("elementId")
driver.find_elements_by_link_text("linkText")
driver.find_elements_by_name("elementName")
driver.find_elements_by_partial_link_text("partialText")
driver.find_elements_by_tag_name("elementTagName")
driver.find_elements_by_xpath("xpath")
```

```python
# now selenium 4.x

from selenium.webdriver.common.by import By

# element
driver.find_element(By.CLASS_NAME,"xx")
driver.find_element(By.CSS_SELECTOR,"xx")
driver.find_element(By.ID,"xx")
driver.find_element(By.LINK_TEXT,"xx")
driver.find_element(By.NAME,"xx")
driver.find_element(By.PARITIAL_LINK_TEXT,"xx")
driver.find_element(By.TAG_NAME,"xx")
driver.find_element(By.XPATH,"xx")

# elements
driver.find_elements(By.CLASS_NAME,"xx")
driver.find_elements(By.CSS_SELECTOR,"xx")
driver.find_elements(By.ID,"xx")
driver.find_elements(By.LINK_TEXT,"xx")
driver.find_elements(By.NAME,"xx")
driver.find_elements(By.PARITIAL_LINK_TEXT,"xx")
driver.find_elements(By.TAG_NAME,"xx")
driver.find_elements(By.XPATH,"xx")
```

---

## wait

### explicit wait

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Firefox()
driver.get("http://somedomain/url_that_delays_loading")
wait = WebDriverWait(driver, 10)  # sec

try:
    element = wait.until(EC.element_to_be_clickable((By.ID, 'someid')))
finally:
    driver.quit()
```

```text
title_is
title_contains
presence_of_element_located
visibility_of_element_located
visibility_of
presence_of_all_elements_located
text_to_be_present_in_element
text_to_be_present_in_element_value
frame_to_be_available_and_switch_to_it
invisibility_of_element_located
element_to_be_clickable
staleness_of
element_to_be_selected
element_located_to_be_selected
element_selection_state_to_be
element_located_selection_state_to_be
alert_is_present
```

### implict wait

```python
from selenium import webdriver

driver = webdriver.Firefox()
driver.implicitly_wait(10)  # seconds
driver.get("http://somedomain/url_that_delays_loading")
myDynamicElement = driver.find_element_by_id("myDynamicElement")
```

---

## page object model

```python
# util.py
import os

from selenium import webdriver
from selenium.webdriver.common.by import By

MainPageLocatorDict = {
    'about': (By.ID, 'about'),
    'downloads': (By.ID, 'downloads'),
    'documentation': (By.ID, 'documentation'),
}

def create_driver(host="127.0.0.1", port=4444):
    server_host = host
    server_port = port

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument(
        f"--crash-dumps-dir={os.path.expanduser('~/tmp/Crashpad')}")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Remote(
        command_executor=f'http://{server_host}:{server_port}/wd/hub',
        options=chrome_options)
    driver.set_window_size(1920, 1200)
    # driver.maximize_window()
    print("window size:", driver.get_window_size())

    return driver
```

```python
# page.py
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from util import MainPageLocatorDict

class BasePage():
    def __init__(self, driver, ):
        self.driver = driver
        self.timeout = 30

    def find_element(self, *locator):
        return self.driver.find_element(*locator)

    def open(self, url):
        self.driver.get(url)

    def get_title(self):
        return self.driver.title

    def get_url(self):
        return self.driver.current_url

    def find_visible_elem(self, locator, timeout=10):
        self
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def find_clickable_elem(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

    def capture_screen(self, pic):
        self.driver.save_screenshot(pic)

    def quit(self):
        self.driver.quit()

class MainPage(BasePage):
    def __init__(self, driver):
        self.locator_dict = MainPageLocatorDict
        super().__init__(driver)

    def get_id_about(self):
        return self.find_visible_elem(self.locator_dict["about"])
```

```python
# main.py
from util import create_driver
from page import MainPage

url = "https://www.python.org/"
driver = create_driver()
driver.get(url)

page = MainPage(driver)
id = page.get_id_about()
print(f"{id.text}, tag: {id.tag_name}")
page.quit()
```

---

## code generator

### selenium ide

[Selenium IDE for chrome](https://chromewebstore.google.com/detail/selenium-ide/mooikfkahbdckldjjndioackbalphokd)
[Selenium IDE for firefox](https://addons.mozilla.org/en-US/firefox/addon/selenium-ide/)
[Selenium IDE for edge](https://microsoftedge.microsoft.com/addons/detail/selenium-ide/ajdpfmkffanmkhejnopjppegokpogffp)
[Selenium IDE](https://github.com/SeleniumHQ/selenium-ide/releases)

### katalon recorder

[Katalon Recorder for chome](https://chrome.google.com/webstore/detail/katalon-recorder-selenium/ljdobmomdgdljniojadhoplhkpialdid)
[Katalon Recorder for firefox](https://addons.mozilla.org/en-US/firefox/addon/katalon-automation-record/)
[Katalon Recorder for edge](https://microsoftedge.microsoft.com/addons/detail/katalon-recorder-seleniu/hdodkejagjkdomgbiioijegfmiiknoam)

---

## HAR

HAR / HTTP Archive

### mitmproxy

BrowserMob Proxy (java8 or java 11) -> browserup-proxy -> mitmproxy

```bash
linux:~ $ pip install mitmproxy     # mitmproxy=11.0.2
linux:~ $ mitmproxy --version

# test
linux:~ $ mitmweb
linux:~ $ curl http://127.0.0.1:8081
```

step 1.

```python
# http_export.py
import json
from mitmproxy import http

class HTTPExport:
    def __init__(self):
        self.data = []

    def request(self, flow: http.HTTPFlow) -> None:
        print(f"Captured request: {flow.request.url}")
        self.data.append({
            "method": flow.request.method,
            "url": flow.request.url,
            "headers": dict(flow.request.headers),
            "request_body": flow.request.text,
        })

    def response(self, flow: http.HTTPFlow) -> None:
        print(f"Captured response: {flow.request.url}")
        if self.data:
            self.data[-1].update({
                "status_code": flow.response.status_code,
                "response_headers": dict(flow.response.headers),
                "response_body": flow.response.text,
            })

    def done(self):
        print("Saving HTTP data...")
        with open("http_data.json", "w") as f:
            json.dump(self.data, f, indent=4)
        print("HTTP data saved to http_data.json")

addons = [HTTPExport()]
```

```bash
linux:~ $ mitmdump -s http_export.py
```

step 2.

```bash
# demo.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

proxy_address = "127.0.0.1:8080"  # mitmproxy address

# ChromeOptions with proxy
chrome_options = Options()
chrome_options.add_argument(f'--proxy-server={proxy_address}')
chrome_options.add_argument('--ignore-certificate-errors')

# WebDriver
webdriver_path = '/usr/local/bin/chromedriver'
service = Service(webdriver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

url = "https://www.example.com"
driver.get(url)

print(driver.title)
driver.quit()
```

```bash
linux:~ $ python3 demo.py
```

### cdp

CDP / Chrome DevTools Protocol

```python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import json

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

webdriver_path = '/usr/local/bin/chromedriver'
service = Service(executable_path=webdriver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    devtools = driver.execute_cdp_cmd
    devtools("Performance.enable", {})

    url = "https://www.example.com"
    driver.get(url)
    time.sleep(5)

    metrics = devtools("Performance.getMetrics", {})
    print("Performance Metrics:")
    print(json.dumps(metrics, indent=2))

    file_path = "performance_metrics.json"
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(metrics, file, indent=2)
    print(f"Performance metrics saved to {file_path}")

    devtools("Performance.disable", {})

finally:
    driver.quit()
```

---

## grid

### hub

```bash
hub:~ # java -jar ./selenium-server-4.22.0.jar hub [--port 4444]

# check defult port 4444
hub:~ # curl -L http://localhost:4444
hub:~ # ss -lutnp | grep 4444
```

### node

```bash
node:~ # java -jar ./selenium-server-4.22.0.jar node [--hub http://<hub>:4444]
```

### client

```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def run_test_on_grid():
    grid_url = "http://localhost:4444/wd/hub"

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-gpu")

    driver = webdriver.Remote(
        command_executor=grid_url,
        options=chrome_options
    )

    try:
        driver.get("https://example.com")
        print("Page title is:", driver.title)

        driver.find_element(
            "xpath", "//a[text()='More information...']").click()
        print("Current URL after click:", driver.current_url)
    finally:
        driver.quit()

if __name__ == "__main__":
    # single browser
    run_test_on_grid()

    # multiple browser
    processes = [multiprocessing.Process(
        target=run_test_on_grid) for _ in range(2)]

    for process in processes:
        process.start()

    for process in processes:
        process.join()
```

---

## ref

[The Selenium Browser Automation Project](https://www.selenium.dev/documentation/)
[Selenium with Python](https://selenium-python.readthedocs.io/index.html)
[mitmproxy](https://mitmproxy.org/)
[mitmproxy - github](https://github.com/mitmproxy/mitmproxy)
