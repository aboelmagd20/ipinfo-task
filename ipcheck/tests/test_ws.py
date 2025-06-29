import pytest
from channels.testing import WebsocketCommunicator
from channels.layers import get_channel_layer
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User
from ipinfo_project.asgi import application
from asgiref.sync import sync_to_async


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_websocket_connection_and_data():
    @sync_to_async
    def create_or_get_test_user():

        User.objects.filter(email='mo@dphish.com').delete()
        return User.objects.create_user(email='mo@dphish.com', password='12345678')

    user = await create_or_get_test_user()

    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    communicator = WebsocketCommunicator(
        application,
        f"/ws/ip-info/?token={access_token}"
    )

    connected, _ = await communicator.connect()
    assert connected is True

    channel_layer = get_channel_layer()
    await channel_layer.group_send(
        f"user_{user.id}",
        {
            "type": "send_ip_info",
            "data": {
                "ip": "8.8.8.8",
                "country": "US",
                "city": "New York",
                "org": "Google LLC"
            }
        }
    )

    response = await communicator.receive_json_from()
    assert response["ip"] == "8.8.8.8"
    assert response["country"] == "US"
    assert response["city"] == "New York"
    assert response["org"] == "Google LLC"

    await communicator.disconnect()
