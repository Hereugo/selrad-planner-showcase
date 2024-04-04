from django.urls import include, path
from rest_framework import routers

from api.managers.views import ManagerViewSet


router = routers.DefaultRouter()

router.register(r"managers", ManagerViewSet)

urlpatterns = [path("", include(router.urls))]
