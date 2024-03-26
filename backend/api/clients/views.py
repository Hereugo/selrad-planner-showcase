import logging

from rest_framework.viewsets import ModelViewSet

from clients.models import Client
from .serializers import ClientSerializer 


logger = logging.getLogger(__name__)


class ClientViewSet(ModelViewSet):
    """API для работы с клиентами."""

    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    pagination_class = None

