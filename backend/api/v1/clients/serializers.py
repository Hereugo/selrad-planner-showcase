from rest_framework import serializers

from django.db import transaction

from clients.models import Address, Client, MetaClient


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
            "twogis_link",
            "lon",
            "lat",
            "created_at",
            "updated_at",
        )


class AddressCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating Address model."""

    lon = serializers.FloatField()
    lat = serializers.FloatField()
    twogis_link = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = Address
        fields = (
            "street",
            "twogis_link",
            "lon",
            "lat",
        )


class MetaClientSerializer(serializers.ModelSerializer):
    """Serializer for MetaClient model."""

    id = serializers.StringRelatedField()

    class Meta:
        model = MetaClient
        fields = (
            "id",
            "name",
            "created_at",
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


class ClientCreateSerializer(serializers.ModelSerializer):
    """Serializer for atomically creating a shop with address."""

    meta_client_id = serializers.PrimaryKeyRelatedField(
        queryset=MetaClient.objects.all(),
        source="meta_client",
        required=False,
        write_only=True,
    )
    meta_client_name = serializers.CharField(required=False, write_only=True)
    address = AddressCreateSerializer(write_only=True)

    class Meta:
        model = Client
        fields = (
            "id",
            "name",
            "meta_client_id",
            "meta_client_name",
            "address",
        )
        read_only_fields = ("id",)

    def validate(self, attrs):
        has_meta_client = attrs.get("meta_client") is not None
        has_meta_client_name = bool(attrs.get("meta_client_name"))

        if has_meta_client == has_meta_client_name:
            raise serializers.ValidationError(
                "Передайте ровно одно поле: meta_client_id или meta_client_name."
            )

        return attrs

    @transaction.atomic
    def create(self, validated_data):
        address_data = validated_data.pop("address")
        meta_client_name = validated_data.pop("meta_client_name", None)

        if meta_client_name:
            meta_client = MetaClient.objects.filter(
                name__iexact=meta_client_name.strip()
            ).first()
            if meta_client is None:
                meta_client = MetaClient.objects.create(name=meta_client_name.strip())
            validated_data["meta_client"] = meta_client

        address = Address.objects.create(**address_data)
        return Client.objects.create(address=address, **validated_data)

    def to_representation(self, instance):
        return ClientSerializer(
            instance,
            context={"request": self.context.get("request")},
        ).data
