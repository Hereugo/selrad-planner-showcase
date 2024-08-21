from django_filters import (
    FilterSet,
    DateFilter,
    ModelMultipleChoiceFilter,
    BooleanFilter,
)


from managers.models import Manager
from plans.models import Plan, WorkItem, PlanWorkItem


class TaskFilter(FilterSet):
    start_date = DateFilter(field_name="plan__assigned_date", lookup_expr=("gte"))
    end_date = DateFilter(field_name="plan__assigned_date", lookup_expr=("lte"))

    class Meta:
        model = PlanWorkItem
        fields = [
            "start_date",
            "end_date",
        ]


class PlanFilter(FilterSet):
    start_date = DateFilter(field_name="assigned_date", lookup_expr=("gte"))
    end_date = DateFilter(field_name="assigned_date", lookup_expr=("lte"))
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
