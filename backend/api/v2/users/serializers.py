import logging

from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from api.v1.users.serializers import ManagerSerializer as APIv1ManagerSerializer

logger = logging.getLogger(__name__)


class ManagerSerializer(APIv1ManagerSerializer):
    permissions = serializers.SerializerMethodField(read_only=True)

    @extend_schema_field(serializers.ListField(child=serializers.CharField()))
    def get_permissions(self, obj):
        return obj.user.get_all_permissions() if obj.user else []
