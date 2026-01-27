"""Urls are defined here for party purposes"""

from django.urls import path

from apps.party.api.views import (
    JoinParty,
    MyParty,
    Party,
    PartyInfo
)

urlpatterns = [
    path("", Party.as_view()),
    path("join", JoinParty.as_view()),
    path("<uuid:id>", PartyInfo.as_view()),
    path("me", MyParty.as_view()),
]