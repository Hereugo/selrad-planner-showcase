from django.urls import include, path
from rest_framework import routers

from api.plans.views import (
    PlanViewSet,
    WorkItemViewSet,
    TaskViewSet,
    PaymentRegistryViewSet,
)


router = routers.DefaultRouter()

router.register(r"work_items", WorkItemViewSet)
router.register(r"plans", PlanViewSet)
router.register(r"tasks", TaskViewSet)
router.register(r"payment_registries", PaymentRegistryViewSet)

urlpatterns = [path("", include(router.urls))]
