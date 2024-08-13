from django_filters import FilterSet, DateFilter, ModelMultipleChoiceFilter


from managers.models import Manager
from plans.models import Plan, PlanWorklist, WorkItem


class TaskFilter(FilterSet):
    start_date = DateFilter(field_name="plan__assigned_date", lookup_expr=("gte"))
    end_date = DateFilter(field_name="plan__assigned_date", lookup_expr=("lte"))

    class Meta:
        model = PlanWorklist
        fields = [
            "start_date",
            "end_date",
        ]


class PlanFilter(FilterSet):
    start_date = DateFilter(field_name="assigned_date", lookup_expr=("gte"))
    end_date = DateFilter(field_name="assigned_date", lookup_expr=("lte"))
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

    class Meta:
        model = Plan
        fields = [
            "start_date",
            "end_date",
            "work_items",
            "managers",
        ]
