# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.consumer import SyncConsumer,AsyncConsumer
from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import StopConsumer

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        # join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        
        self.accept()

    def disconnect(self, close_code):
        # leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,self.channel_name
        )
        
    # receive messages from websocket
    def receive(self, text_data):
        print(text_data)
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # send message to room group
        self.channel_layer.group_send(
            self.room_group_name,{"type":"chat.message","message":message}
        )
        
        # self.send(text_data=json.dumps({"message": message}))
        
    # receive message from room group
    def chat_message(self,event):
        message = event["message"]
        
        # send message to websocket
        self.send(text_data = json.dumps({"message":message}))
        
        
class MySyncConsumer(AsyncConsumer):
    
    async def websocket_connect(self,event):
        print('Websocket Conected...',event)
        print('\nchannel layer...',self.channel_layer)
        print('\nchannel name...',self.channel_name)
        # for every instance of this consumer there would be a unique channel layer and channel name
        # adding this instance channel to a group called programmers
        # here we are adding this channel to the group on connecting to websocket server.
        await self.channel_layer.group_add('programmers',self.channel_name)
        self.send({
            'type':'websocket.accept'
        })
        
        
        
    async def websocket_receive(self,event):
        print('Websocket received from client...',event)
        print('Type of Message Received from the client..','type(event) ',type(event),"type(event['text'])",type(event['text']))
        # send message to the group
        await self.channel_layer.group_send('programmers',{
            'type':'chat.message',
            'message':event['text']
        })
        
        
    async def websocket_disconnect(self,event):
        print('Websocket disconnected...',event)
        print('\nchannel layer...',self.channel_layer)
        print('\nchannel name...',self.channel_name)
        await self.channel_layer.group_discard(
            'programmers',
            self.channel_name
        )
        raise StopConsumer()
    
    
    def chat_message(self,event):
        print('event..',event)
        #  sending message to client
        self.send({
            'type':'websocket.send',
            'text': event['message']
        })
        
        