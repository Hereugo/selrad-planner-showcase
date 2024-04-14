from django_filters import FilterSet, DateFilter, NumberFilter
from django.db.models import Q, Value
from django.db.models.functions import Concat

from plans.models import Plan


class PlanFilter(FilterSet):
    date_after = DateFilter(field_name="assigned_date", lookup_expr=("gte"))
    date_before = DateFilter(field_name="assigned_date", lookup_expr=("lte"))
    worklist_id = NumberFilter(field_name="worklist_id", method="filter_worklist_id")
    manager_id = NumberFilter(field_name="manager_id", method="filter_manager_id")

    def filter_worklist_id(self, queryset, name, value):
        return queryset.filter(worklist__id=value)

    def filter_manager_id(self, queryset, name, value):
        return queryset.filter(managers__id=value)

    class Meta:
        model = Plan
        fields = [
            "date_after",
            "date_before",
            "worklist_id",
            "manager_id",
        ]
