"""Party Views are defined here"""
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.party.api.serializers import JoinPartySerializer, PartyRegistrationSerializer


class Party(APIView):
    """
    Party dtails and creation takes place here
    """
    permission_classes = [IsAuthenticated]
    def post(self, request):
        """
        User post request for registration
        """
        serializer = PartyRegistrationSerializer(data=request.data, context={"request":request})
        if serializer.is_valid():
            serializer.save()
            return Response({'msg' : 'Party created Successfully' }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class JoinParty(APIView):
    """
    Party details and creation takes place here
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Docstring for post
        """
        serializer = JoinPartySerializer(
            data=request.data,
            context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"msg": "Joined party successfully"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MyParty(APIView):
    """
    This will return the party details in which user is a leader
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Docstring for get
        """
        party = Party.objects.filter(leader=request.user)
        if not party:
            return Response({"msg": "No party found"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = PartyRegistrationSerializer(data=party)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PartyInfo(APIView):
    """
    This will return details of particular party using id in query params
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        """
        Docstring for get
        """
        party = Party.objects.get(id=id)
        serializer = PartyRegistrationSerializer(party)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
