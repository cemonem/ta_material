import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import app.misc

class SimulationConsumer(WebsocketConsumer):
    groups = ["users"]

    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        rect_pos = json.loads(text_data)
        print(rect_pos)
        with app.misc.lock:
            app.misc.rect_pos["x"] = rect_pos["x"]
            app.misc.rect_pos["y"] = rect_pos["y"]
        async_to_sync(self.channel_layer.group_send)("users", {'type': 'broadcast_msg', 'message': rect_pos})

    def broadcast_msg(self, event):
        self.send(text_data=json.dumps(event["message"]))
