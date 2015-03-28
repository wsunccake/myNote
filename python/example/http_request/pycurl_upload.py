import pycurl

url = 'http://localhost/upload.php'
filename = '/tmp/abc'

web_site = pycurl.Curl()
web_site.setopt(pycurl.URL, url)
web_site.setopt(pycurl.HTTPPOST, [("upload_file", (web_site.FORM_FILE, filename) )] )
web_site.perform()
web_site.close()