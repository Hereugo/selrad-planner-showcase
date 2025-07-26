import logging

from django_filters import (
    BooleanFilter,
    DateFilter,
    FilterSet,
    ModelMultipleChoiceFilter,
)

from plans.models import PlanWorkItem, WorkItem

logger = logging.getLogger(__name__)


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
    content_types = ModelMultipleChoiceFilter(
        queryset=WorkItem.objects.all(),
        field_name="content_type__model",
        to_field_name="meta_name",
        method="filter_content_types",
        help_text="Enter list of content_type model names: (shipment, photo, return), default filtered by shipment only",
    )
    mine = BooleanFilter(
        method="filter_mine",
        help_text="False or default value filters by requested user, else don't apply filter.",
    )

    def filter_content_types(self, queryset, name, value):
        if value:
            return queryset.filter(work_item__in=value)
        return queryset

    def filter_mine(self, queryset, name, value):
        logger.error(value)
        if value:
            return queryset.filter(plan__managers__user=self.request.user)
        return queryset

    class Meta:
        model = PlanWorkItem
        fields = [
            "start_date",
            "end_date",
            "content_types",
            "mine",
        ]
