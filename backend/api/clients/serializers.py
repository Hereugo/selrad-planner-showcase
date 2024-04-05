from rest_framework import serializers
from clients.models import Client, Address


class AddressSerializer(serializers.ModelSerializer):
    """Serializer for Address model"""

    class Meta:
        model = Address
        fields = (
            "id",
            "street",
            "lon",
            "lat",
            "created_at",
            "updated_at",
        )


class ClientSerializer(serializers.ModelSerializer):
    """Serializer for Client model"""

    addresses = AddressSerializer(read_only=True, many=True)

    class Meta:
        model = Client
        fields = (
            "id",
            "name",
            "created_at",
            "updated_at",
            "addresses",
        )
