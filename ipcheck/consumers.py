import json
from channels.generic.websocket import AsyncWebsocketConsumer
import logging

logger = logging.getLogger(__name__)

class IPInfoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.group_name = None

        if self.user.is_authenticated:
            self.group_name = f"user_{self.user.id}"
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()
            logger.info(f"[WS] Connected user: {self.user.id}")
        else:
            await self.close()

    async def disconnect(self, close_code):
        if self.channel_layer and self.group_name:
            await self.channel_layer.group_discard(self.group_name, self.channel_name)
            logger.info(f"[WS] Disconnected user: {self.user.id}")

    async def send_ip_info(self, event):
        await self.send(text_data=json.dumps(event["data"]))
