__author__ = 'rex8312'

import websocket  # pip install websocket-client
import json

if __name__ == '__main__':
    websocket.enableTrace(True)
    ws = websocket.create_connection("ws://127.0.0.1:8888/chatsocket")
    print("Sending 'Hello, World'...")
    try:
        while True:
            data = raw_input()
            ws.send(json.dumps({'body': '{}'.format(data)}))
            result = ws.recv()
            print result['body']
    except KeyboardInterrupt:
        ws.close()
