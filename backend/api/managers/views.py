import logging

from rest_framework.viewsets import ModelViewSet

from managers.models import Manager
from .serializers import ManagerSerializer


logger = logging.getLogger(__name__)


class ManagerViewSet(ModelViewSet):
    """API для работы с менеджерами."""

    queryset = Manager.objects.filter(is_hidden=False)
    serializer_class = ManagerSerializer
    pagination_class = None
