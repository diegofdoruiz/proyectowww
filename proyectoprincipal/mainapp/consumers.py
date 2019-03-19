# import asyncio
# import json
# from django.contrib.auth import get_user_model
# from channels.auth import  AuthMiddleware, get_user, login, logout
# from channels.consumer import AsyncConsumer
# from channels.db import database_sync_to_async

# from .models import Thread, ChatMessage

# class ChatConsumer(AsyncConsumer):
# 	async def websocket_connect(self, event):
# 		# print("connected", event)
# 		other_user = self.scope['url_route']['kwargs']['username']
# 		me = self.scope['user']
# 		#print(other_user, me)
# 		thread_obj = await self.get_thread(me, other_user)
# 		self.thread_obj = thread_obj
# 		chat_room = f"thread_{thread_obj.id}"
# 		self.chat_room = chat_room
# 		await self.channel_layer.group_add(
# 			chat_room,
# 			self.channel_name
# 		)
# 		await self.send({
# 			"type": "websocket.accept"
# 		})

# 	async def websocket_receive(self, event):
# 		#print("receive", event)
# 		fron_text = event.get('text', None)
# 		if fron_text is not None:
# 			loaded_dict_data = json.loads(fron_text)
# 			msg = loaded_dict_data.get('message')
# 			#print(msg)
# 			user = self.scope['user']
# 			username = 'default'
# 			if user.is_authenticated:
# 				username = user.username
# 			myResponse = {
# 				'message': msg,
# 				'username': username
# 			}

# 			await self.create_chat_message(user, msg)

# 			# broadcast the message event to be sent
# 			await self.channel_layer.group_send(
# 				self.chat_room,
# 				{
# 					"type": "chat_message",
# 					"text": json.dumps(myResponse)
# 				} 
# 			)

# 	async def chat_message(self, event):
# 		#send the actual message
# 		await self.send({
# 			"type": "websocket.send",
# 			"text": event['text']
# 		})


# 	async def websocket_disconnect(self, event):
# 		pass

# 	@database_sync_to_async
# 	def get_thread(self, user, other_user):
# 		return Thread.objects.get_or_new(user, other_user)[0]

# 	@database_sync_to_async
# 	def create_chat_message(self, me, msg):
# 		thread_obj = self.thread_obj
# 		return ChatMessage.objects.create(thread=thread_obj, user=me, message=msg)	

# chat/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        print(self.scope['user'])
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = self.scope['user']
        username = 'default'
        if user.is_authenticated:
        	username = user.username

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))
