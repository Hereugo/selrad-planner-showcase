import logging
from datetime import datetime
from typing import Optional

from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from rest_framework.request import Request

from managers.models import GeoPoint, Manager

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
    # Optional GPS fix time (ISO 8601). Invalid/missing → server now.
    created_at = serializers.CharField(
        required=False,
        allow_null=True,
        allow_blank=True,
    )

    class Meta:
        model = GeoPoint
        exclude = ("point",)
        read_only_fields = (
            "id",
            "manager",
        )

    def create(self, validated_data):
        raw_created_at = validated_data.pop("created_at", None)
        validated_data["manager"] = self.context["request"].user.manager

        created_at = self._parse_client_datetime(raw_created_at)
        if created_at is not None:
            validated_data["created_at"] = created_at

        return super().create(validated_data)

    def _parse_client_datetime(self, raw) -> Optional[datetime]:
        if raw is None or raw == "":
            return None
        if isinstance(raw, datetime):
            dt = raw
        else:
            dt = parse_datetime(str(raw))
            if dt is None:
                logger.warning("Ignoring invalid geopoint created_at: %r", raw)
                return None
        # Project runs with USE_TZ=False; store naive UTC datetimes.
        if timezone.is_aware(dt):
            dt = timezone.make_naive(dt)
        return dt

    def to_representation(self, instance):
        return GeoPointSerializer(
            instance, context={"request": self.context.get("request")}
        ).data


class ManagerSerializer(serializers.ModelSerializer):
    id = serializers.StringRelatedField()
    geopoints = serializers.SerializerMethodField()

    class Meta:
        model = Manager
        exclude = (
            "user",
            "is_hidden",
        )

    @extend_schema_field(GeoPointSerializer(many=True))
    def get_geopoints(self, obj):
        request: Optional[Request] = self.context.get("request")

        # limit the number of geopoints returned
        geo_limit = int(request.query_params.get("geo_limit", 5) if request else 5)

        qs = obj.geopoints.all()[:geo_limit]

        return GeoPointSerializer(qs, many=True).data

    @extend_schema_field(serializers.ListField(child=serializers.CharField()))
    def get_permissions(self, obj):
        return obj.user.get_all_permissions() if obj.user else []


class MeSerializer(ManagerSerializer):
    permissions = serializers.SerializerMethodField(read_only=True)

    @extend_schema_field(serializers.ListField(child=serializers.CharField()))
    def get_permissions(self, obj):
        return obj.user.get_all_permissions() if obj.user else []
