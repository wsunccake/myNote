import urllib

query_args = {'NAME_PHP': 'user', 'AGE_PHP': 12}
encoded_args = urllib.urlencode(query_args)
url = 'http://localhost/post.php'

web_site = urllib.urlopen(url)

print 'http header:/n', web_site.info()
print 'http status:', web_site.getcode()
print 'url:', web_site.geturl()

for line in web_site:
    print line,
web_site.close()