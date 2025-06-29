from django.db import models

class IPInfo(models.Model):
    submitted_by = models.ForeignKey('users.User', on_delete=models.CASCADE, null=True, blank=True)
    ip = models.GenericIPAddressField()
    country = models.CharField(max_length=100, null=True, blank=True)
    region = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    org = models.CharField(max_length=255, null=True, blank=True)
    loc = models.CharField(max_length=100, null=True, blank=True)
    processed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.ip
