import logging

from django_filters import BooleanFilter, FilterSet

from managers.models import Manager

logger = logging.getLogger(__name__)


class UserFilter(FilterSet):
    get_all = BooleanFilter(
        method="filter_get_all",
        help_text="False or default value only shows viewable managers, on true also shows hidden managers.",
    )

    def filter_get_all(self, queryset, name, value):
        if value:
            return queryset
        return queryset.filter(is_hidden=False)

    class Meta:
        model = Manager
        fields = [
            "get_all",
        ]
