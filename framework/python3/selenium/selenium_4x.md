# selenium 4

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

crash-dumps-dir
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
```

---

## ref

[The Selenium Browser Automation Project](https://www.selenium.dev/documentation/)
[Selenium with Python](https://selenium-python.readthedocs.io/index.html)
