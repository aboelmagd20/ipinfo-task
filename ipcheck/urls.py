from django.urls import path
from .views import SubmitIPsView, IPInfoListView

urlpatterns = [
    path('submit-ips/', SubmitIPsView.as_view(), name='submit-ips'),
    path('ip-infos/', IPInfoListView.as_view(), name='ip-info-list'),
]
