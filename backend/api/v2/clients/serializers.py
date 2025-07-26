from rest_framework import serializers

from api.v1.clients.serializers import ClientSerializer as APIv1ClientSerializer
from clients.models import Client, MetaClient


class MetaClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = MetaClient
        fields = ("name",)


class ClientSerializer(APIv1ClientSerializer):
    """Serializer for Client model"""

    meta_client = MetaClientSerializer(read_only=True, many=False)

    class Meta:
        model = Client
        fields = (
            "id",
            "name",
            "created_at",
            "updated_at",
            "address",
            "is_hidden_on_map",
            "meta_client",
        )
