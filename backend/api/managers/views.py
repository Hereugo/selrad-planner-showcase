import logging

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from managers.models import Manager

from .serializers import ManagerSerializer
from .custom_filters import ManagerFilter


logger = logging.getLogger(__name__)


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
