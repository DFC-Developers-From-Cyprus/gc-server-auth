from django.urls import path

from .viewsets import VolunteerViewSet, OrganizationViewSet, AuthViewSet

urlpatterns = [
    path(
        "volunteer/register/",
        VolunteerViewSet.as_view({"post": "create"}),
        name="volunteer-register",
    ),
    path(
        "organization/register/",
        OrganizationViewSet.as_view({"post": "create"}),
        name="organization-register",
    ),
    path(
        "auth/login/",
        AuthViewSet.as_view({"post": "login"}),
        name="login",
    ),
    path(
        "auth/logout/",
        AuthViewSet.as_view({"post": "logout"}),
        name="logout",
    ),
]
