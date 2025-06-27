import uuid

from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import CustomUser
from .serializers import LoginSerializer, RegistrationSerializer


@method_decorator(csrf_protect, name="create")
class LoginViewSet(viewsets.ViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

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
    permission_classes = [AllowAny]

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
