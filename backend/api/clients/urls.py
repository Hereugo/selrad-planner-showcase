from django.urls import include, path
from rest_framework import routers

from api.clients.views import ClientViewSet


router = routers.DefaultRouter()

router.register(r"clients", ClientViewSet)

urlpatterns = [path("", include(router.urls))]
