"""Model for User details"""
from datetime import datetime, timedelta
import random
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    """
    CustomUser Model with UUID as its primary key
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_exp = models.DateTimeField(blank=True, null=True)
    otp_verified = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.first_name} {self.last_name} "

    def generate_otp(self):
        """Function to generate otp"""
        self.otp = str(random.randint(100000, 999999))
        self.otp_exp = datetime.now() + timedelta(minutes=2)
        self.otp_verified = False
        self.save()
