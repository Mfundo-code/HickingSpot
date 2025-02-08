# consumers.py (for Django Channels)

import json
from channels.generic.websocket import WebsocketConsumer

class RideConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        data = json.loads(text_data)
        self.send(text_data=json.dumps({'message': 'Notification received'}))
