from rest_framework import serializers
from .models import IPInfo

class IPInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = IPInfo
        fields = '__all__'
