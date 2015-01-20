__author__ = 'rex8312'

"""
websocket을 이용한 간단한 클라이언트
python의 websocket 클라이언트 이용
# pip install websocket-client
"""

import websocket
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
            result = json.loads(result)
            print result['body']
    except KeyboardInterrupt:
        ws.close()
