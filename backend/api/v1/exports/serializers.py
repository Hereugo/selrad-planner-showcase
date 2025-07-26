from rest_framework import serializers

from managers.models import Manager
from plans.models import WorkItem


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

    only_shipment = serializers.BooleanField(
        required=False, help_text="Output plans only with shipment work_item"
    )
    ordering = serializers.CharField(
        required=False, help_text="Which field to use when ordering the results."
    )
    search = serializers.CharField(required=False, help_text="A search term")

    work_items = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=WorkItem.objects.all(),
        required=False,
        help_text="Enter work_item ids that a plan must include (inclusively)",
    )
    managers = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Manager.objects.all(),
        required=False,
        help_text="Enter manager ids that a plan must include (inclusively)",
    )

    def validate(self, attrs):
        start_date = attrs.get("start_date", None)
        end_date = attrs.get("end_date", None)

        if start_date and end_date and start_date > end_date:
            raise serializers.ValidationError()

        return super().validate(attrs)


class ManagerFilterSerializer(serializers.Serializer):
    manager = serializers.PrimaryKeyRelatedField(
        queryset=Manager.objects.all(),
        required=True,
        help_text="Enter manager id (overrides managers parameter)",
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
    comment = serializers.CharField(
        required=False,
        help_text="Enter a comment that is displayed under dispatch list.",
        default="",
    )
    set_time_dispatch = serializers.BooleanField(
        required=False, default=True, help_text="Save the time when dispatch was done."
    )

    def validate_manager_id(self, manager):
        if not manager.is_driver:
            raise serializers.ValidationError()

        return manager


class ReportFilterSerializer(BaseFilterSerializer, ManagerFilterSerializer):
    pass


class PaymentReportFilterSerializer(BaseFilterSerializer):
    pass
