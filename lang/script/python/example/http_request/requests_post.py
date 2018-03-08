import requests

url = 'http://localhost/post.php'
payload = { 'NAME_PHP': 'abc',
            'AGE_PHP': 123
}

web_site = requests.post(url, data = payload)

print web_site.content