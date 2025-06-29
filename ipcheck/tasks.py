from celery import shared_task
import requests
from .models import IPInfo
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

@shared_task
def fetch_ip_info(ip, user_id):
    try:
        url = f"https://ipinfo.io/{ip}/json"
        response = requests.get(url, timeout=5)
        data = response.json()

        record = IPInfo.objects.create(
            ip=ip,
            submitted_by_id=user_id,
            country=data.get("country"),
            region=data.get("region"),
            city=data.get("city"),
            org=data.get("org"),
            loc=data.get("loc"),
            processed=True
        )


        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"user_{user_id}",
            {
                "type": "send_ip_info",
                "data": {
                    "ip": record.ip,
                    "country": record.country,
                    "city": record.city,
                    "org": record.org,
                }
            }
        )
    except Exception as e:
        print(f"Error processing {ip}: {e}")
