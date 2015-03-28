import urllib

url = 'http://localhost/get.php?name_php=abc&age_php=10'

print urllib.urlopen(url).read()