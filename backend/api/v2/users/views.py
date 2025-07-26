import logging

from api.v1.users.views import UserViewSet as APIv1UserViewSet
from api.v2.users.custom_filters import UserFilter
from api.v2.users.serializers import ManagerSerializer
from managers.models import Manager

logger = logging.getLogger(__name__)


class UserViewSet(APIv1UserViewSet):
    """API v2 для работы с пользователями."""

    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer
    filterset_class = UserFilter
