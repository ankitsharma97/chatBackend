from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
from channels.exceptions import StopConsumer
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            request_user = self.scope['user']
            if request_user.is_authenticated:
                chat_with_user = self.scope['url_route']['kwargs']['id']
                user_ids = [int(request_user.id), int(chat_with_user)]
                user_ids.sort()
                if chat_with_user == 0 or chat_with_user == '0':
                    await self.close()
                self.room_name = f'chat_{user_ids[0]}_{user_ids[1]}'
                
                
                await self.channel_layer.group_add(
                    self.room_name,
                    self.channel_name
                )
                await self.accept()
            else:
                await self.close()
        except Exception as e:
            raise StopConsumer(f"Error during connect: {e}")
            await self.close()

    async def receive(self, text_data):
        try:
            data ={
                "message": text_data
            }
            data = json.dumps(data)
            data = json.loads(data)
            message = data['message']

            await self.save_message(message, self.scope['user'].id, self.scope['url_route']['kwargs']['id'])
            
            await self.channel_layer.group_send(
                self.room_name,
                {
                    'type': 'chat_message',
                    'message': message
                }
            )
        except json.JSONDecodeError as e:
            raise StopConsumer(f"Error decoding JSON: {e}")
        except KeyError as e:
            raise StopConsumer(f"Error decoding JSON: {e}")
        except Exception as e:
            raise StopConsumer(f"Error during receive: {e}")

    async def disconnect(self, close_code):
        try:
            await self.channel_layer.group_discard(
                self.room_name,
                self.channel_name
            )
        except Exception as e:
            raise StopConsumer(f"Error during disconnect: {e}")

    async def chat_message(self, event):
        try:
            message = event['message']
            await self.send(text_data=message)
        except Exception as e:
            raise StopConsumer(f"Error during chat_message: {e}")

    @database_sync_to_async
    def save_message(self, message, sender_id, receiver_id):
        from chat.models import Chat
        from account.models import User
        try:
            sender = User.objects.get(id=sender_id)
            receiver = User.objects.get(id=receiver_id)
            Chat.objects.create(message=message, sender=sender, receiver=receiver)
        except User.DoesNotExist as e:
            raise StopConsumer(f"Error saving message: {e}")
        except Exception as e:
            raise StopConsumer(f"Error saving message: {e}")
