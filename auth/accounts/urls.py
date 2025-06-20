from django.urls import path

from .viewsets import RegistrationViewSet

urlpatterns = [
    path(
        "registration/",
        RegistrationViewSet.as_view({"post": "create"}),
        name="user-register",
    ),
]
