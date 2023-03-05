from asgiref.sync import async_to_sync, sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import StopConsumer
from channels.db import database_sync_to_async
from .models import Coordinates
import json


class DriverBehaviourReceiver(AsyncWebsocketConsumer):
    """
    AsyncWebsocketConsumer subclass that receives data from a websocket and saves it to the database.
    """

    async def connect(self):
        """
        Called when a websocket is initiated. Adds the user to a group and accepts the websocket connection.
        """
        if not self.scope['user']:
            await self.close()
            raise StopConsumer()

        self.room_name = self.scope['user']
        self.room_group_name = "con_%s" % self.room_name
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        """
        Called when a websocket is disconnected. Removes the user from the group.
        """
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        """
        Called when a message is received from the websocket. Saves the data to the database and sends a message to the group.
        """
        text_data = json.loads(text_data)
        await sync_to_async(Coordinates.objects.create)(
            user_id=self.scope['user'],
            x_coordinate=text_data.get("x"),
            y_coordinate=text_data.get("y"),
            z_coordinate=text_data.get("z")
        )
        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "chat_message", "message": "created"}
        )

    async def chat_message(self, event):
        """
        Called when a message is received from the group. Sends the message to the websocket.
        """
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))

    async def send_data(self, event):
        """
        Sends data from the database to the websocket.
        """
        data = await self._get_model()
        await self.send(text_data=json.dumps({"message": data}))

    @database_sync_to_async
    def _get_model(self):
        """
        Async function that gets data from the database and returns it.
        """
        return list(Coordinates.objects.filter(user_id=self.scope['user']).values())
