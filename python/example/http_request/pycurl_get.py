import pycurl

url = 'http://localhost/get.php?name_php=abc&age_php=12'

web_site = pycurl.Curl()
web_site.setopt(pycurl.URL, url)
web_site.setopt(pycurl.VERBOSE, 0)
web_site.perform()
web_site.close()