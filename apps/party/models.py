"""
Party related models are defined here
"""
import random
from django.db import IntegrityError, models
from apps.users.models import CustomUser

class Party(models.Model):
    """
    Model which store the details of users with the party
    """
    party_leader = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    party_name = models.CharField(max_length='20')
    party_description = models.CharField(max_length='250')
    party_code = models.CharField(max_length='6', unique=True, editable=False)

    def save(self, *args, **kwargs):
        while True:
            self.party_code = self._generate_party_code()
            try:
                super().save(*args, **kwargs)
                break
            except IntegrityError:
                self.party_code = None
        if self.party_code:
            return super().save(*args, **kwargs)

    def _generate_party_code(self):
        """Function to generate team code """
        char_list = list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789")
        team_code = ''
        for _ in range(6):
            team_code = team_code + random.choice(char_list)
        return team_code

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
