from rest_framework import serializers

from clients.models import Address, Client


class AddressSerializer(serializers.ModelSerializer):
    """Serializer for Address model"""

    id = serializers.StringRelatedField()
    lon = serializers.FloatField()
    lat = serializers.FloatField()

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

    id = serializers.StringRelatedField()
    address = AddressSerializer(read_only=True, many=False)

    class Meta:
        model = Client
        fields = (
            "id",
            "name",
            "created_at",
            "updated_at",
            "address",
            "is_hidden_on_map",
        )
