import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    surname = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    profile_picture = models.URLField(
        blank=True,
        null=True,
    )
    email = models.EmailField(
        unique=True,
        blank=False,
        null=False,
    )
    role = models.CharField(
        max_length=50,
        choices=[
            ("volunteer", "Volunteer"),
            ("organization", "Organization"),
        ],
        blank=False,
        null=False,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return self.email
