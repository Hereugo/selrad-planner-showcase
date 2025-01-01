from django_filters import (
    BooleanFilter,
    DateFilter,
    FilterSet,
    ModelMultipleChoiceFilter,
)
from managers.models import Manager
from plans.models import PaymentRegistry, Plan, PlanWorkItem, WorkItem


class PaymentRegistryFilter(FilterSet):
    start_date = DateFilter(
        field_name="date",
        lookup_expr=("gte"),
        help_text="Enter start date in YYYY-MM-DD format",
    )
    end_date = DateFilter(
        field_name="date",
        lookup_expr=("lte"),
        help_text="Enter end date in YYYY-MM-DD format",
    )
    managers = ModelMultipleChoiceFilter(
        queryset=Manager.objects.all(),
        field_name="manager__id",
        to_field_name="id",
    )
    is_confirmed = BooleanFilter(field_name="is_confirmed")

    class Meta:
        model = PaymentRegistry
        fields = [
            "start_date",
            "end_date",
            "managers",
            "is_confirmed",
        ]


class TaskFilter(FilterSet):
    start_date = DateFilter(
        field_name="plan__assigned_date",
        lookup_expr=("gte"),
        help_text="Enter end date in YYYY-MM-DD format",
    )
    end_date = DateFilter(
        field_name="plan__assigned_date",
        lookup_expr=("lte"),
        help_text="Enter end date in YYYY-MM-DD format",
    )

    class Meta:
        model = PlanWorkItem
        fields = [
            "start_date",
            "end_date",
        ]


class PlanFilter(FilterSet):
    start_date = DateFilter(
        field_name="assigned_date",
        lookup_expr=("gte"),
        help_text="Enter start date in YYYY-MM-DD format",
    )
    end_date = DateFilter(
        field_name="assigned_date",
        lookup_expr=("lte"),
        help_text="Enter start date in YYYY-MM-DD format",
    )
    only_shipment = BooleanFilter(method="filter_only_shipment")
    work_items = ModelMultipleChoiceFilter(
        queryset=WorkItem.objects.all(),
        field_name="work_items__id",
        to_field_name="id",
    )
    managers = ModelMultipleChoiceFilter(
        queryset=Manager.objects.all(),
        field_name="managers__id",
        to_field_name="id",
    )

    def filter_only_shipment(self, queryset, name, value):
        if value:
            return queryset.filter(work_items__content_type__model="shipment")
        return queryset

    class Meta:
        model = Plan
        fields = ["start_date", "end_date", "work_items", "managers", "only_shipment"]
