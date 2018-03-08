import requests

s = requests.Session()
url = 'http://localhost/session'
payload = {'username': 'testuser',
           'password': 'test1234',
           'submit': 'Yes'
}

s1 = s.post(url + '/login.php', data=payload)
print s1.status_code
print s1.text
s2 = s.get(url + '/get.php')
print s2.text