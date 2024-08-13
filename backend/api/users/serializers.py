import logging

from django.contrib.auth import get_user_model
from rest_framework import serializers

from api.managers.serializers import RoleSerializer


User = get_user_model()
logger = logging.getLogger(__name__)


class UserSerializer(serializers.ModelSerializer):
    """Сериализация пользователя"""

    id = serializers.StringRelatedField()
    roles = RoleSerializer(source="manager.roles", many=True, read_only=True)
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "permissions",
            "roles",
        )
        read_only_fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "permissions",
        )

    def get_permissions(self, obj):
        return obj.get_all_permissions()
