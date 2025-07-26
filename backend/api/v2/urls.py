from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    path("", include("api.v2.clients.urls")),
    path("", include("api.v2.plans.urls")),
    path("", include("api.v2.users.urls")),
]
