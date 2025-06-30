from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
import ipaddress
from rest_framework.permissions import IsAuthenticated

from .models import IPInfo
from .serializers import IPInfoSerializer
from .tasks import fetch_ip_info


class SubmitIPsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        ip_list = request.data.get('ips', [])
        total_ips = len(ip_list)
        valid_ips = []

        for ip in ip_list:
            try:
                ipaddress.ip_address(ip.strip())
                valid_ips.append(ip.strip())
            except ValueError:
                continue

        for ip in valid_ips:
            fetch_ip_info.delay(ip, request.user.id)

        ignored_ips_count = total_ips - len(valid_ips)

        return Response({
            "status": "processing",
            "total_ips": total_ips,
            "valid_ips_count": len(valid_ips),
            "ignored_ips_count": ignored_ips_count,
            "submitted_ips": valid_ips,
        }, status=status.HTTP_202_ACCEPTED)


class IPInfoListView(generics.ListAPIView):
    serializer_class = IPInfoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return IPInfo.objects.filter(submitted_by=self.request.user)
