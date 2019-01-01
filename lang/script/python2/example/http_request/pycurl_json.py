import pycurl
import json

url = "http://localhost/json.php"
data = json.dumps({"name": "abc", "age": 123})

web_site = pycurl.Curl()
web_site.setopt(pycurl.URL, url)
web_site.setopt(pycurl.POST, 1)
web_site.setopt(pycurl.POSTFIELDS, data)
web_site.perform()
web_site.close()