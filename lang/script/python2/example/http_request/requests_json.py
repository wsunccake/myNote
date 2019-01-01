import requests
import json

url = 'http://localhost/json.php'
payload = {"name": "abc",
           "age": 123
}

web_site = requests.post(url, data = json.dumps(payload) )

print web_site.url
print web_site.content