"""
Party related models are defined here
"""
import uuid
from django.db import  models
from django.utils import timezone
from apps.users.models import CustomUser

class Party(models.Model):
    """
    Model which store the details of users with the party
    """
    class PartyDuration(models.IntegerChoices):
        """Choices for party duration"""
        H1  = 60,   "1 Hour"
        H2  = 120,  "2 Hours"
        H4  = 240,  "4 Hours"
        H8  = 480,  "8 Hours"
        D1  = 1440, "1 Day"
        D3  = 4320, "3 Days"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    duration = models.PositiveSmallIntegerField(
        choices=PartyDuration.choices,
        db_index=True
    )
    leader = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=6, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(
        db_index=True
    )
    @property
    def is_expired(self) -> bool:
        return timezone.now() >= self.expires_at

class PartyMembers(models.Model):
    """
    Model for Party Members
    """
    party = models.ForeignKey(
        Party,
        on_delete=models.CASCADE,
        related_name="Party_details"
    )
    member = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='Member_details'
    )
