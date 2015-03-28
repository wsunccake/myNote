import pycurl

url = 'http://localhost/post.php'
payload = 'NAME_PHP=abc&AGE_PHP=123'

web_site = pycurl.Curl()
web_site.setopt(pycurl.URL, url)
web_site.setopt(pycurl.POSTFIELDS, payload)
web_site.perform()
web_site.close()