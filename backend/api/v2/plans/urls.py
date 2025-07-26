from django.urls import include, path
from rest_framework import routers

from api.v2.plans.views import PlanViewSet, TaskViewSet

router = routers.DefaultRouter()

router.register(r"plans", PlanViewSet)
router.register(r"tasks", TaskViewSet)

urlpatterns = [path("", include(router.urls))]
