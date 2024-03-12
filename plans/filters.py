from django_filters import FilterSet 

from .models import Plan 

class PlanFilter(FilterSet):
    class Meta:
        model = Plan 
        fields = {
            'comment': ['icontains'] 
        }
