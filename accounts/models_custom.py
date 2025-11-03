from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser2Manager(AbstractUser):
    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('email_verified', False)
        return super().create_user(username, email, password, **extra_fields)
    phone_number = models.CharField(max_length=100, blank=True, null=True)
    email_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class CustomUser2(AbstractUser):
    phone_number = models.CharField(max_length=100, blank=True, null=True)
    email_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)
    objects = CustomUser2Manager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    def __str__(self):
        return self.username