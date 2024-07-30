from django_filters.rest_framework import (
    FilterSet,
    ModelMultipleChoiceFilter,
    NumberFilter,
)

from managers.models import Manager, Role


class ManagerFilter(FilterSet):
    managers = ModelMultipleChoiceFilter(
        queryset=Manager.objects.all(),
        field_name="id",
        to_field_name="id",
        conjoined=True,
        always_filter=True,
    )
    roles = ModelMultipleChoiceFilter(
        queryset=Role.objects.all(),
        field_name="roles__id",
        to_field_name="id",
        always_filter=True,
    )
    limit = NumberFilter(field_name="limit")

    class Meta:
        model = Manager
        fields = [
            "managers",
            "roles",
            "limit",
        ]
