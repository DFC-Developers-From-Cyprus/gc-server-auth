from django.urls import path

from .viewsets import LoginViewSet, RegistrationViewSet

urlpatterns = [
    path(
        "login/",
        LoginViewSet.as_view({"post": "create"}),
        name="user-login",
    ),
    path(
        "registration/",
        RegistrationViewSet.as_view({"post": "create"}),
        name="user-register",
    ),
]
