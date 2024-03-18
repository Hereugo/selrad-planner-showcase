from django_filters import FilterSet, CharFilter, DateFilter
from django.db.models import Q, Value
from django.db.models.functions import Concat

from .models import Plan 

class PlanFilter(FilterSet):
    search = CharFilter(method='my_custom_filter')

    date_after = DateFilter(field_name='assigned_date',lookup_expr=('gte'))
    date_before = DateFilter(field_name='assigned_date',lookup_expr=('lte'),) 

    def my_custom_filter(self, queryset, name, value):
        q = Plan.objects.annotate(
            search=Concat('client__name', 'worklist__name', 'managers__first_name')
        )
        q = q.filter(search__icontains=value)
        # remove duplicates in q for sqlite3
        
        st = set(q.values_list('pk', flat=True))
        q = Plan.objects.filter(pk__in=st)

        return q


    class Meta:
        model = Plan 
        fields = [
            'search',
            'date_after',
            'date_before',
        ]
