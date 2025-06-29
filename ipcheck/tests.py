import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from ipcheck.models import IPInfo
from users.models import User  
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.mark.django_db
class TestIPInfoViews:

    def setup_method(self):

        User.objects.filter(email='mo@dphish.com').delete()

        self.user = User.objects.create_user(email='mo@dphish.com', password='12345678')
        self.client = APIClient()

        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_submit_valid_ips(self):
        url = reverse('submit-ips')
        data = {
            "ips": ["8.8.8.8", "1.1.1.1"]
        }
        response = self.client.post(url, data, format='json')
        assert response.status_code == 202
        assert "submitted_ips" in response.data
        assert len(response.data["submitted_ips"]) == 2

    def test_submit_invalid_ips(self):
        url = reverse('submit-ips')
        data = {
            "ips": ["invalid_ip", "999.999.999.999"]
        }
        response = self.client.post(url, data, format='json')
        assert response.status_code == 202
        assert len(response.data["submitted_ips"]) == 0

    def test_get_ip_infos(self):
        IPInfo.objects.create(ip="8.8.8.8", country="US", processed=True, submitted_by=self.user)
        url = reverse('ip-info-list')
        response = self.client.get(url)
        assert response.status_code == 200
        assert len(response.data) >= 1
