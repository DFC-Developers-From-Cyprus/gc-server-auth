import uuid

from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

# from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from .models import (
    Subscribe,
    CustomUser,
)
from .serializers import (
    ProfileSerializer,
    SubscribeSerializer,
    OrganizationSerializer,
    LoginSerializer,
    RegistrationSerializer,
)


class ProfileViewSet(viewsets.ViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = ProfileSerializer

    # def update(self, request, *args, **kwargs):
    #     user_uuid = kwargs.get("uuid")
    #     user = get_object_or_404(CustomUser, uuid=user_uuid)
    #     serializer = self.serializer_class(user, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @method_decorator(csrf_protect, name="retrieve")
    def retrieve(self, request, *args, **kwargs):
        user_uuid = kwargs.get("uuid")

        if not user_uuid:
            return Response(
                {"detail": "User UUID is required."}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user_obj = CustomUser.objects.filter(uuid=user_uuid)
        except CustomUser.DoesNotExist:
            raise NotFound(detail="User not found.")

        if user_obj.first().is_superuser:
            return Response(
                {"detail": "User not found."}, status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ProfileSerializer(user_obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SubscribeViewSet(viewsets.ViewSet):
    queryset = Subscribe.objects.all()
    serializer_class = SubscribeSerializer

    @method_decorator(csrf_protect, name="create")
    def create(self, request, *args, **kwargs):
        new_uuid = uuid.uuid4()
        while Subscribe.objects.filter(uuid=new_uuid).exists():
            new_uuid = uuid.uuid4()

        data = request.data.copy()
        data["uuid"] = str(new_uuid)

        Subscribe.objects.create(
            user_uuid=data["user_uuid"],
            org_uuid=data["org_uuid"],
            uuid=data["uuid"],
        )

        serializer = SubscribeSerializer(data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @method_decorator(csrf_protect, name="retrieve")
    def retrieve(self, request, *args, **kwargs):
        user_uuid = kwargs.get("uuid")

        if not user_uuid:
            return Response(
                {"detail": "User UUID is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user_subscribed_org = Subscribe.objects.filter(user_uuid=user_uuid)
        except Subscribe.DoesNotExist:
            raise NotFound(detail="Subscribe not found.")

        serializer = SubscribeSerializer(user_subscribed_org, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrganizationViewSet(viewsets.ViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = OrganizationSerializer

    @method_decorator(csrf_protect, name="retrieve")
    def retrieve(self, request, *args, **kwargs):
        org_uuid = kwargs.get("uuid")

        if not org_uuid:
            return Response(
                {"detail": "UUID is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            organization = CustomUser.objects.get(uuid=org_uuid)
        except CustomUser.DoesNotExist:
            raise NotFound(detail="Organization not found.")

        serializer = OrganizationSerializer(organization, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @method_decorator(csrf_protect, name="list")
    def list(self, request, *args, **kwargs):
        organizations = CustomUser.objects.filter(role="organization")
        serializer = OrganizationSerializer(organizations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LoginViewSet(viewsets.ViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = LoginSerializer

    @method_decorator(csrf_protect, name="create")
    def create(self, request, *args, **kwargs):
        username = request.data.get("username", "").strip()
        password = request.data.get("password", "").strip()

        if not username or not password:
            return Response(
                {"error": "Both username and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = CustomUser.objects.filter(username=username).first()

        if not user:
            return Response(
                {"error": "Invalid username"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if user.password != password:
            return Response(
                {"error": "Invalid credentials."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        return Response(
            {
                "uuid": user.uuid,
                "username": user.username,
                "email": user.email,
                "role": user.role,
            },
            status=status.HTTP_200_OK,
        )


@method_decorator(csrf_protect, name="create")
class RegistrationViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = RegistrationSerializer

    @method_decorator(csrf_protect, name="create")
    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        new_uuid = uuid.uuid4()
        while CustomUser.objects.filter(uuid=new_uuid).exists():
            new_uuid = uuid.uuid4()

        data["uuid"] = str(new_uuid)

        password = data.get("password", "").strip()
        username = data.get("username", "").strip()
        email = data.get("email", "").strip().lower()
        role = data.get("role", "").strip()

        if not username or not email or not password or not role:
            return Response(
                {"error": "All fields (username, email, password, role) are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if CustomUser.objects.filter(username=username).exists():
            return Response(
                {"username": "This username is already taken."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if CustomUser.objects.filter(email=email).exists():
            return Response(
                {"email": "This email is already registered."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            validate_password(password)
        except ValidationError as e:
            return Response(
                {"password": e.messages}, status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        message = f"User '{username}' ({email}) with role '{role}' has been successfully created."

        return Response({"message": message}, status=status.HTTP_201_CREATED)
