import logging

from rest_framework.viewsets import ReadOnlyModelViewSet

from api.utils.custom_permissions import IsAuthenticated

from clients.models import Client
from .serializers import ClientSerializer


logger = logging.getLogger(__name__)


class ClientViewSet(ReadOnlyModelViewSet):
    """API для работы с клиентами."""

    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    pagination_class = None
