import urllib

url = 'http://localhost/file.dat'
filename = 'file.dat'

urllib.urlretrieve(url, filename)