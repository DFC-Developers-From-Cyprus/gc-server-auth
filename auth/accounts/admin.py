from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    # Fields shown when editing a user
    fieldsets = UserAdmin.fieldsets + (
        (
            _("Additional Info"),
            {
                "fields": (
                    "name",
                    "surname",
                    "profile_picture",
                    "role",
                )
            },
        ),
    )

    # Fields shown when creating a user
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            _("Additional Info"),
            {
                "fields": (
                    "name",
                    "surname",
                    "profile_picture",
                    "email",
                    "role",
                )
            },
        ),
    )

    list_display = (
        "uuid",
        "username",
        "email",
        "name",
        "surname",
        "profile_picture",
        "role",
        "created_at",
        "updated_at",
    )

    search_fields = ("uuid", "username", "email", "name", "role")
    ordering = ("created_at",)
    readonly_fields = ("created_at", "updated_at")
