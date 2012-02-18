try:
	import http.client as httplib
except:
	import httplib
try:
	import urllib.request as request
	import urllib.parse as parse 
except:
	import urllib as request
	import urllib as parse
	import urllib2
	# JEREMY SHOULD FUCKING DIE
	request.build_opener = urllib2.build_opener
	request.HTTPCookieProcessor = urllib2.HTTPCookieProcessor
try:
	import http.cookiejar as cookiejar
except:
	import cookielib as cookiejar

import sys


headers = { "Content-type": "application/x-www-form-urlencoded","Accept": "text/plain" }
url = "/cas/login?service=https%3a%2f%2fwlan.berkeley.edu%2fcgi-bin%2flogin%2fcalnet.cgi%3fsubmit%3dCalNet%26url%3d"

def connect():
        conn = httplib.HTTPSConnection("auth.berkeley.edu")
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
                f = open("data.txt", "U")
                un_pas = str(f.read()).split("\n")
                assert len(un_pas) == 2
                username, password = un_pas
                assert username
                assert password
                f.close()
        except:
                print("Could not open file data.txt, please create data.txt with username and password separated by one newline")
                sys.exit(1)

        values = { "username": username, "password": password, "lt":hidden, "_eventId":"submit" }

    	print username,"   ", password,"    ",len(username)," ",len(password)
        data = parse.urlencode(values)

        conn = httplib.HTTPSConnection("auth.berkeley.edu")
        conn.request("POST", url, data, headers)
        response = conn.getresponse()

        #if authentication sucessfull they send us to candyland for cookies
        if response.status != 302:
            if "The CalNet ID and/or Passphrase you provided are incorrect." in str(response.read()):
                raise Exception("rong username/password")
            else:
                raise Exception("the fuck happened")
        print response.getheaders()
        print 'yoyyoyoyo'

#sometimes i rike cappital and sometim i rike rower case
        bettaHeadda= [ (i[0].lower(),i[1]) for i in response.getheaders() ]


        theURL = dict(bettaHeadda)["location"]
        conn.close()

        #print(f.read())
        print('\n', theURL,"\n\n\n\n")


        #bears need cookies to eat or else they get sad D:
        cj = cookiejar.CookieJar() 
        opener = request.build_opener(request.HTTPCookieProcessor(cj))
        r = opener.open(theURL)
        #print(r.read())
		
def main():
	connect()
if __name__=="__main__":
	main()
	
