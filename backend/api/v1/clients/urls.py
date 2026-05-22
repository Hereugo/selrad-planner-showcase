from django.urls import include, path
from rest_framework import routers

from api.v1.clients.views import ClientViewSet, MetaClientViewSet

router = routers.DefaultRouter()

router.register(r"clients", ClientViewSet)
router.register(r"meta_clients", MetaClientViewSet)

urlpatterns = [path("", include(router.urls))]
