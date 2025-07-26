import logging

from api.v1.plans.views import PlanViewSet as APIv1PlanViewSet
from api.v1.plans.views import TaskViewSet as APIv1TaskViewSet
from api.v2.plans.custom_filters import TaskFilter
from api.v2.plans.serializers import PlanSerializer
from plans.models import PlanWorkItem

logger = logging.getLogger(__name__)


class PlanViewSet(APIv1PlanViewSet):
    serializer_class = PlanSerializer


class TaskViewSet(APIv1TaskViewSet):
    queryset = PlanWorkItem.objects.all()
    filterset_class = TaskFilter

    def get_queryset(self):
        return super(APIv1TaskViewSet, self).get_queryset()
