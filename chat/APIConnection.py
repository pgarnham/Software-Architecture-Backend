from websocket import create_connection
import json
from datetime import datetime

def APIPOST(room, content, user):
    ws = create_connection(f"ws://localhost:8000/ws/chat/{room}/")
    print("Sending POST")
    ws.send(json.dumps({'message':content, 'username':user, 'origin': 'API'}))
    print("Sent")
    ws.close()
