from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(blank=True, max_length=255)
    gender = models.CharField(blank=False, default="M", max_length=1)

    def __str__(self):
        return f"Profile for {self.user.username}"

