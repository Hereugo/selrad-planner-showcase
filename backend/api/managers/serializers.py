from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from managers.models import Manager, GeoPoint


class GeoPointSerializer(serializers.ModelSerializer):
    id = serializers.StringRelatedField()
    manager = serializers.StringRelatedField()

    class Meta:
        model = GeoPoint
        exclude = ("point",)


class GeoPointCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeoPoint
        exclude = ("point",)
        read_only_fields = ("id", "created_at", "manager")


class ManagerSerializer(serializers.ModelSerializer):
    id = serializers.StringRelatedField()
    geopoints = serializers.SerializerMethodField()
    roles = serializers.StringRelatedField(many=True)

    class Meta:
        model = Manager
        exclude = ("user",)

    @extend_schema_field(GeoPointSerializer(many=True))
    def get_geopoints(self, obj):
        request = self.context.get("request", {})
        qs = obj.geopoints.all().limit(request.get("limit", 5))
        return GeoPointSerializer(qs, many=True).data
