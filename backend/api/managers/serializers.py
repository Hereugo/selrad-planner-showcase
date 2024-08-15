from typing import Optional
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from rest_framework.request import Request
from managers.models import Manager, GeoPoint, Role


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
    manager = serializers.PrimaryKeyRelatedField(queryset=Manager.objects.all())

    class Meta:
        model = GeoPoint
        exclude = ("point",)
        read_only_fields = ("id", "created_at", "manager")

    def to_representation(self, instance):
        return GeoPointSerializer(
            instance, context={"request": self.context.get("request")}
        ).data


class RoleSerializer(serializers.ModelSerializer):
    id = serializers.StringRelatedField()

    class Meta:
        model = Role
        fields = (
            "id",
            "name",
        )


class ManagerSerializer(serializers.ModelSerializer):
    id = serializers.StringRelatedField()
    geopoints = serializers.SerializerMethodField()
    roles = RoleSerializer(many=True)

    class Meta:
        model = Manager
        exclude = ("user",)

    @extend_schema_field(GeoPointSerializer(many=True))
    def get_geopoints(self, obj):
        request: Optional[Request] = self.context.get("request")

        # limit the number of geopoints returned
        geo_limit = int(request.query_params.get("geo_limit", 5) if request else 5)

        qs = obj.geopoints.all()[:geo_limit]

        return GeoPointSerializer(qs, many=True).data
