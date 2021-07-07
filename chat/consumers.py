import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message, User
from channels.db import database_sync_to_async
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from datetime import datetime
from allauth.socialaccount.models import SocialAccount
from allauth.app_settings import USER_MODEL
from asgiref.sync import sync_to_async
from .models import Room
from cryptography.fernet import Fernet
from iluovo.settings import FIELD_ENCRYPTION_KEY

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self, room_name  = ''):
        print("CONNECTION ACCEPTED!")
        self.room_name = room_name if room_name != '' else self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        await self.join_group()
        await self.accept()

    async def join_group(self):
        # Join room group
        self.room = await database_sync_to_async(Room.objects.get)(name=self.room_name)
        self.accepted = not self.room.is_private 
        print('')

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )



    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        print("RECEIVE")
        

        text_data_json = json.loads(text_data)


        user = await database_sync_to_async(User.objects.get)(email=text_data_json['email'])



        if 'permission' in text_data_json:
            if text_data_json['email'] == self.room.author:
                await database_sync_to_async(self.room.accepted_users.add)(user)
            else:

                await self.channel_layer.group_send(
                            self.room_group_name,
                            {   
                                'sender_channel_name':self.channel_name,
                                'type': 'permission_request',
                                'message': f"{text_data_json['email']} quiere entrar a esta sala ...",
                                'author':text_data_json['email'],
                                'room': self.room_name,
                                'timestamp': '',
                            }
                        )
            return


        elif 'permission_accepted' in text_data_json:
            await database_sync_to_async(self.room.accepted_users.add)(user)
            return

        if self.room.is_private:
            accepted_users = await database_sync_to_async(self.room.accepted_users.filter)(email=user.email)
            accepted_users_count = await database_sync_to_async(accepted_users.count)()
            if accepted_users_count == 0:
                print('not accepted lil bitch')
                return

        F = Fernet(FIELD_ENCRYPTION_KEY)

        encrypted_message = F.encrypt(bytes(text_data_json['message'],encoding= 'utf-8'))
        message = text_data_json['message']
        timestamp = datetime.now().strftime("%H:%M:%S")
        room = self.room_name
        if 'origin' not in text_data:
            author = await database_sync_to_async(User.objects.get)(email = text_data_json['email'])
            object = Message(author = author, content = encrypted_message, room = room)
            await database_sync_to_async(object.save)()
        else:
            author = await database_sync_to_async(User.objects.get)(id=json.loads(text_data_json['username'])['id'])
        author = author.username

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'author':author,
                'room': room,
                'timestamp': timestamp,
            }
        )

       
        # Send message to room group

 
    # Receive message from room group
    async def chat_message(self, event):
        print('message received')

        message = event['message']
        author = event['author']
        room = event['room']
        timestamp = event['timestamp']

        event_type = event['type']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'author':author,
            'room': room,
            'timestamp': timestamp,
            'type': event_type,

        }))
    async def permission_request(self, event):
        print('permission requested')
        message = event['message']
        author = event['author']
        room = event['room']
        timestamp = event['timestamp']
        event_type = event['type']
        if self.channel_name == event['sender_channel_name']:
            return
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'author':author,
            'room': room,
            'timestamp': timestamp,
            'type': event_type,

        }))
