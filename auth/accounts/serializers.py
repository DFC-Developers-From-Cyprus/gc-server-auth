from rest_framework import serializers

from .models import Subscribe, CustomUser


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "uuid",
            "last_login",
            "username",
            "first_name",
            "last_name",
            "is_staff",
            "is_active",
            "date_joined",
            "name",
            "surname",
            "profile_picture",
            "email",
            "role",
            "created_at",
            "updated_at",
        ]


class SubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscribe
        fields = [
            "uuid",
            "user_uuid",
            "org_uuid",
        ]


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "uuid",
            "username",
            "email",
            "role",
        ]


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
