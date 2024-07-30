from django_filters import FilterSet, DateFilter, NumberFilter, ModelChoiceFilter

from managers.models import Manager
from plans.models import Plan, PlanWorklist


class TaskFilter(FilterSet):
    start_date = DateFilter(field_name="plan__assigned_date", lookup_expr=("gte"))
    end_date = DateFilter(field_name="plan__assigned_date", lookup_expr=("lte"))
    manager = ModelChoiceFilter(
        queryset=Manager.objects.all(),
        field_name="plan__managers__id",
        to_field_name="id",
        conjoined=True,
        always_filter=True,
    )

    class Meta:
        model = PlanWorklist
        fields = [
            "manager",
            "start_date",
            "end_date",
        ]


class PlanFilter(FilterSet):
    start_date = DateFilter(field_name="assigned_date", lookup_expr=("gte"))
    end_date = DateFilter(field_name="assigned_date", lookup_expr=("lte"))
    worklist_id = NumberFilter(field_name="worklist_id", method="filter_worklist_id")
    manager_id = NumberFilter(field_name="manager_id", method="filter_manager_id")

    def filter_worklist_id(self, queryset, name, value):
        if value == -1:
            return queryset.filter(worklist__isnull=True)
        return queryset.filter(worklist__id=value)

    def filter_manager_id(self, queryset, name, value):
        if value == -1:
            return queryset.filter(managers__isnull=True)
        return queryset.filter(managers__id=value)

    class Meta:
        model = Plan
        fields = [
            "start_date",
            "end_date",
            "worklist_id",
            "manager_id",
        ]
