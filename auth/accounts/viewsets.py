from django.contrib.auth import authenticate, login, logout

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import *

from .serializers import *


class VolunteerViewSet(viewsets.ModelViewSet):
    # queryset = TODO
    # serializer_class = TODO
    lookup_field = "uuid"

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"message": "The volunteer is registered", "uuid": user.uuid},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrganizationViewSet(viewsets.ModelViewSet):
    # queryset = TODO
    # serializer_class = TODO
    lookup_field = "uuid"

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"message": "The organization is registered", "uuid": user.uuid},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthViewSet(viewsets.ModelViewSet):
    # queryset = TODO
    # serializer_class = TODO
    lookup_field = "uuid"

    @action(detail=False, methods=["post"], url_path="login")
    def login_user(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            role = None
            if hasattr(user, "volunteerprofile"):
                role = "volunteer"
            elif hasattr(user, "organizationprofile"):
                role = "organization"

            return Response(
                {
                    "message": "Success entering the system",
                    "user_id": getattr(user, "uuid", user.id),
                    "username": user.username,
                    "role": role,
                }
            )

        return Response(
            {"error": "Inappropriate accounting data"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    @action(detail=False, methods=["post"], url_path="logout")
    def logout_user(self, request):
        logout(request)
        return Response({"message": "The output is made"})
