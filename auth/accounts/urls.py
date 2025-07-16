from django.urls import path

from .viewsets import (
    ProfileViewSet,
    SubscribeViewSet,
    OrganizationViewSet,
    LoginViewSet,
    RegistrationViewSet,
)

urlpatterns = [
    path(
        "profile-update/<uuid:uuid>/",
        ProfileViewSet.as_view({"put": "update"}),
        name="profile-update",
    ),
    path(
        "profile-detail/<uuid:uuid>/",
        ProfileViewSet.as_view({"get": "retrieve"}),
        name="profile-detail",
    ),
    path(
        "subscribe-user-organization/",
        SubscribeViewSet.as_view({"post": "create"}),
        name="subscribe-user-org",
    ),
    path(
        "subscribe-user-organization-detail/<uuid:uuid>/",
        SubscribeViewSet.as_view({"get": "retrieve"}),
        name="subscribe-user-org-detail",
    ),
    path(
        "organization-detail/<uuid:uuid>/",
        OrganizationViewSet.as_view({"get": "retrieve"}),
        name="org-detail",
    ),
    path(
        "organizations/",
        OrganizationViewSet.as_view({"get": "list"}),
        name="org-list",
    ),
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
