from django.urls import include, path
from rest_framework import routers

from .views import Exports

router = routers.DefaultRouter()

router.register("exports", Exports)

urlpatterns = [path("", include(router.urls))]
