import urllib

url = 'http://localhost/upload.php'
filename = '/tmp/abc'

# f = open(filename, 'rb')
# filebody = f.read()
# f.close()

# data = {'name': 'file', 'upload_file': filebody}
# data = {'upload_file': filebody}
data = {'upload_file': open('/tmp/abc', 'rb')}

web_site = urllib.urlopen(url,urllib.urlencode(data) )
print web_site.read()