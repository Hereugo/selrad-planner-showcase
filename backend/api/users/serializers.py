import logging

from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()
logger = logging.getLogger(__name__)


class UserSerializer(serializers.ModelSerializer):
    """Сериализация пользователя"""

    role = serializers.SerializerMethodField()
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "permissions",
            "role",
        )
        read_only_fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "permissions",
        )

    def get_role(self, obj):
        return obj.manager.role.name if obj.manager else None

    def get_permissions(self, obj):
        return obj.get_all_permissions()
