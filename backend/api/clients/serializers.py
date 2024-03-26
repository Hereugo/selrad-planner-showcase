from rest_framework import serializers
from clients.models import Client, Address


class AddressSerializer(serializers.ModelSerializer):
    """Serializer for Address model"""
    class Meta:
        model = Address
        fields = (
            'pk',
            'street',
            'lon',
            'lat',
            'created_at',
            'updated_at',
        )


class ClientSerializer(serializers.ModelSerializer):
    """Serializer for Client model"""
    address = AddressSerializer(read_only=True)

    class Meta:
        model = Client
        fields = (
            'pk',
            'name',
            'created_at',
            'updated_at',
            'address',
        )
