from django.urls import include, path
from rest_framework import routers

from api.plans.views import (PlanViewSet, WorklistViewSet)


router = routers.DefaultRouter()

router.register(r'worklist', WorklistViewSet)
router.register(r'plans', PlanViewSet)

urlpatterns = [
    path('', include(router.urls))
]
