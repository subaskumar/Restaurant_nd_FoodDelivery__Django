from channels.generic.websocket import AsyncWebsocketConsumer
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync,sync_to_async
import json
from .models import *

class OrderProgress(WebsocketConsumer):
    
    def connect(self):
        self.user = self.scope['user']
        self.room_name = self.scope['url_route']['kwargs']['user_id']
        self.room_group_name = 'user_%s' % self.room_name
        
        print(self.room_group_name)
        print(self.room_group_name)
        print("consumer connected")
        print(self.channel_layer)
        
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        if self.user.is_authenticated:
            self.accept()
            order = OrderPlace.give_order_details(self.room_name)
            
            self.send(text_data=json.dumps({
                'payload': order
            }))
        else:
            self.close()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        
    def order_status(self, event):
        print(event)
        print("ok received")
        order = event['value']
        print(order)
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'payload': order
        }))