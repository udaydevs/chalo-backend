"""Party related serializers are defined here"""
import random
# pylint: disable=E1101
from datetime import timedelta
from rest_framework import serializers
from django.utils import timezone
from django.db import IntegrityError, transaction
from django.db.models import Q
from apps.party.models import Party, PartyMembers
from apps.users.api.serializers import CustomUser, UserSerializer

class PartyRegistrationSerializer(serializers.ModelSerializer):
    """This serializer is for the creation of party"""
    is_expired = serializers.SerializerMethodField()

    class Meta:
        """
        The behaviours of fields are defined here
        """
        model = Party
        fields = (
            "id",
            "name",
            "leader",
            "duration",
            "code",
            "created_at",
            "expires_at",
            "is_expired",
        )
        read_only_fields = ("id", "leader", "code", "created_at", "expires_at", "is_expired")

    def create(self, validated_data):
        validated_data["leader"] = self.context["request"].user
        validated_data["expires_at"] = timezone.now() + timedelta(
            minutes=validated_data["duration"]
        )

        for _ in range(5):
            validated_data["code"] = self._generate_code()
            try:
                with transaction.atomic():
                    return Party.objects.create(**validated_data)
            except IntegrityError:
                continue

        raise serializers.ValidationError(
            "Could not generate a unique party code"
        )
    def get_is_expired(self, obj):
        """This will get value of is_expired from the computed field"""
        return obj.is_expired

    def _generate_code(self):
        """Function to generate team code """
        char_list = list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789")
        team_code = ''
        for _ in range(6):
            team_code = team_code + random.choice(char_list)
        return team_code

class JoinPartySerializer(serializers.ModelSerializer):
    """
    Docstring for JoinPartySerializer
    """
    code = serializers.CharField(write_only=True)

    class Meta:
        """
        Docstring for Meta
        """
        model = PartyMembers
        fields = ("code",)

    def validate_code(self, value):
        """
        Docstring for validate_code
        """
        user = self.context["request"].user
        try:
            party = Party.objects.get(code=value)
        except Party.DoesNotExist as e:
            raise serializers.ValidationError(f"Invalid party code: {e}")

        if party.is_expired:
            raise serializers.ValidationError("Party has expired")

        if PartyMembers.objects.filter(Q(member=user)|Q( party__leader=user)).exists():
            raise serializers.ValidationError("Already joined this party")
        self.context["party"] = party
        return value

    def create(self, validated_data):
        return PartyMembers.objects.create(
            party=self.context["party"],
            member=self.context["request"].user
        )
class LeaderMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id", "username", "email")
class PartyInfoSerializer(serializers.ModelSerializer):
    leader = LeaderMiniSerializer(read_only=True)

    class Meta:
        model = Party
        fields = (
            "id",
            "name",
            "leader",
            "duration",
            "code",
            "created_at",
            "expires_at",
        )
