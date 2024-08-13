import logging

from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
)

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from managers.models import Manager

from .serializers import ManagerSerializer
from .custom_filters import ManagerFilter


logger = logging.getLogger(__name__)


@extend_schema_view(
    list=extend_schema(
        description="Получить список менеджеров",
        filters=True,
        parameters=[
            OpenApiParameter(
                name="geo_limit",
                type=int,
                required=False,
            )
        ],
    ),
)
class ManagerViewSet(mixins.ListModelMixin, GenericViewSet):
    """API для работы с менеджерами."""

    queryset = Manager.objects.filter(is_hidden=False)
    serializer_class = ManagerSerializer
    filterset_class = ManagerFilter
    pagination_class = None

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context
