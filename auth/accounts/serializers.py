from rest_framework import serializers

from .models import CustomUser


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "password",
            "username",
        ]


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "password",
            "username",
            "email",
            "role",
        ]
