import requests

url = 'http://localhost/upload.php'
files = {'upload_file': open('/tmp/abc', 'rb')}

web_site = requests.post(url, files = files)

print web_site.content
print web_site.status_code
print web_site.headers
print web_site.text