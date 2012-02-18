import http.client
import urllib.request, urllib.parse
import http.cookiejar

import sys


headers = { "Content-type": "application/x-www-form-urlencoded","Accept": "text/plain" }
url = "/cas/login?service=https%3a%2f%2fwlan.berkeley.edu%2fcgi-bin%2flogin%2fcalnet.cgi%3fsubmit%3dCalNet%26url%3d"


conn = http.client.HTTPSConnection("auth.berkeley.edu")
conn.request("GET", url)
response = conn.getresponse()


shit = str(response.read())
startString = 'input type="hidden" name="lt" value="'
endString = '" />\\n\\t\\t\\t\\t\\t\\t\\t<input type="hidden" name="_eventId"'

start = len(startString)+shit.find(startString)
end = shit.find(endString)

hidden = shit[start:end]

#print(hidden,"\n\n\n\n\n")
#import pdb; pdb.set_trace()
try:
	f = open("data.txt")
	un_pas = str(f.read()).split("\n")
	assert len(un_pas) == 2
	username, password = un_pas
	assert username
	assert password
except:
	print("Could not open file data.txt, please create data.txt with username and password separated by one newline")
	sys.exit(1)

values = { "username": username, "password": password, "lt":hidden, "_eventId":"submit" }

data = urllib.parse.urlencode(values)

conn = http.client.HTTPSConnection("auth.berkeley.edu")
conn.request("POST", url, data, headers)
response = conn.getresponse()
if response.status != 302:
    if "The CalNet ID and/or Passphrase you provided are incorrect." in str(response.read()):
        raise Exception("rong username/password")
    else:
        raise Exception("the fuck happened")

theURL = dict(response.getheaders())["Location"]
conn.close()

#print(f.read())
print('\n', theURL,"\n\n\n\n")

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
r = opener.open(theURL)
print(r.read())
