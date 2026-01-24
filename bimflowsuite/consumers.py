import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from celery.result import AsyncResult
from asgiref.sync import sync_to_async

class TaskProgressConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.task_id = self.scope['url_route']['kwargs']['task_id']
        self.group_name = f'task_{self.task_id}'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        # Handle client pings if needed
        pass

    async def task_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'task_update',
            'status': event['status'],
            'progress': event['progress'],
        }))

# Broadcast from Celery (in tasks.py)
@sync_to_async
def broadcast_progress(task_id, status, progress):
    # Use channel_layer to send
    pass