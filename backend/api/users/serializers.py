import logging
from typing import Optional

from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from rest_framework.request import Request

from managers.models import Manager, GeoPoint


User = get_user_model()
logger = logging.getLogger(__name__)


class GeoPointSerializer(serializers.ModelSerializer):
    id = serializers.StringRelatedField()
    manager = serializers.StringRelatedField()
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()

    class Meta:
        model = GeoPoint
        exclude = ("point",)


class GeoPointCreateSerializer(serializers.ModelSerializer):
    id = serializers.StringRelatedField()

    class Meta:
        model = GeoPoint
        exclude = ("point",)
        read_only_fields = (
            "id",
            "created_at",
            "manager",
        )

    def create(self, validated_data):
        validated_data["manager"] = self.context["request"].user.manager
        return super().create(validated_data)

    def to_representation(self, instance):
        return GeoPointSerializer(
            instance, context={"request": self.context.get("request")}
        ).data


class ManagerSerializer(serializers.ModelSerializer):
    id = serializers.StringRelatedField()
    geopoints = serializers.SerializerMethodField()

    class Meta:
        model = Manager
        exclude = ("user", "is_hidden", "is_driver", "is_manager", "is_keeper")

    @extend_schema_field(GeoPointSerializer(many=True))
    def get_geopoints(self, obj):
        request: Optional[Request] = self.context.get("request")

        # limit the number of geopoints returned
        geo_limit = int(request.query_params.get("geo_limit", 5) if request else 5)

        qs = obj.geopoints.all()[:geo_limit]

        return GeoPointSerializer(qs, many=True).data


class MeSerializer(ManagerSerializer):
    permissions = serializers.SerializerMethodField(read_only=True)

    @extend_schema_field(serializers.ListField(child=serializers.CharField()))
    def get_permissions(self, obj):
        return obj.user.get_all_permissions() if obj.user else []
