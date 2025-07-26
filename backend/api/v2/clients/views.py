import logging

from api.v1.clients.views import ClientViewSet as APIv1ClientViewSet
from api.v2.clients.serializers import ClientSerializer

logger = logging.getLogger(__name__)


class ClientViewSet(APIv1ClientViewSet):
    serializer_class = ClientSerializer
    pass
