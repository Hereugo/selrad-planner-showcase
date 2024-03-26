from django_filters import FilterSet, CharFilter, DateFilter
from django.db.models import Q, Value
from django.db.models.functions import Concat

from plans.models import Plan 


class PlanFilter(FilterSet):
    date_after = DateFilter(field_name='assigned_date', lookup_expr=('gte'))
    date_before = DateFilter(field_name='assigned_date', lookup_expr=('lte')) 

    class Meta:
        model = Plan 
        fields = [
            'date_after',
            'date_before',
        ]

