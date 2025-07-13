from django.urls import path

from .viewsets import (
    ProfileViewSet,
    SubscribeViewSet,
    OrganizationViewSet,
    LoginViewSet,
    RegistrationViewSet,
)

urlpatterns = [
    # path(
    #     "profile/<uuid:uuid>/",
    #     ProfileViewSet.as_view({"put": "update"}),
    #     name="profile-update",
    # ),
    path(
        "profile/<uuid:uuid>/",
        ProfileViewSet.as_view({"get": "retrieve"}),
        name="profile-detail",
    ),
    path(
        "subscribe/",
        SubscribeViewSet.as_view({"post": "create"}),
        name="subscribe-user-org",
    ),
    path(
        "subscribe/<uuid:uuid>/",
        SubscribeViewSet.as_view({"get": "retrieve"}),
        name="subscribe-user-org-detail",
    ),
    path(
        "org/<uuid:uuid>/",
        OrganizationViewSet.as_view({"get": "retrieve"}),
        name="org-detail",
    ),
    path(
        "orgs/",
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
