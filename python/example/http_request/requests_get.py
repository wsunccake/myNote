import requests

url = 'http://localhost/get.php'
payload = { 'name_php': 'abc',
            'age_php': 123
}

web_site = requests.get(url, params = payload)

print web_site.url
print web_site.content