from django.urls import path

from .viewsets import ViewSet

urlpatterns = [
    path(
        "/",
        ViewSet.as_view({"post": "create"}),
        name="create",
    ),
    path(
        "/",
        ViewSet.as_view({"get": "retrieve"}),
        name="detail",
    ),
    path(
        "/",
        ViewSet.as_view({"get": "list"}),
        name="list",
    ),
]
