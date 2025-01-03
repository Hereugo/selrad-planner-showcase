from managers.models import Manager
from rest_framework import serializers


class BaseFilterSerializer(serializers.Serializer):
    """Serializer for query params"""

    start_date = serializers.DateField(
        required=False,
        help_text="Enter start date in YYYY-MM-DD format",
    )
    end_date = serializers.DateField(
        required=False,
        help_text="Enter start date in YYYY-MM-DD format",
    )

    def validate(self, attrs):
        start_date = attrs.get("start_date", None)
        end_date = attrs.get("end_date", None)

        if start_date and end_date and start_date > end_date:
            raise serializers.ValidationError()

        return super().validate(attrs)


class ManagerFilterSerializer(serializers.Serializer):
    manager = serializers.PrimaryKeyRelatedField(
        queryset=Manager.objects.all(), required=True
    )


class CompareYearsFilterSerializer(BaseFilterSerializer):
    to_year_diff = serializers.IntegerField(default=1)
    start_date = serializers.DateField(
        required=True,
        help_text="Enter start date in YYYY-MM-DD format",
    )
    end_date = serializers.DateField(
        required=True,
        help_text="Enter start date in YYYY-MM-DD format",
    )

    def validate_to_year_diff(self, to_year_diff: int):
        if to_year_diff < 0:
            raise serializers.ValidationError()

        return to_year_diff


class DispatchListFilterSerializer(BaseFilterSerializer, ManagerFilterSerializer):
    comment = serializers.CharField(required=False)
    set_time_dispatch = serializers.BooleanField(required=False, default=True)

    def validate_manager_id(self, manager):
        if not manager.is_driver:
            raise serializers.ValidationError()

        return manager


class ReportFilterSerializer(BaseFilterSerializer, ManagerFilterSerializer):
    pass
