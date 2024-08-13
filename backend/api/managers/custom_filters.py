from django_filters.rest_framework import (
    FilterSet,
    ModelMultipleChoiceFilter,
)

from managers.models import Manager, Role


class ManagerFilter(FilterSet):
    managers = ModelMultipleChoiceFilter(
        queryset=Manager.objects.all(),
        field_name="id",
        to_field_name="id",
    )
    roles = ModelMultipleChoiceFilter(
        queryset=Role.objects.all(),
        field_name="roles__id",
        to_field_name="id",
    )

    class Meta:
        model = Manager
        fields = [
            "managers",
            "roles",
        ]
