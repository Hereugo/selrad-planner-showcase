from django import forms
from .models import Plan


class PlanForm(forms.ModelForm):
    class Meta:
        model = Plan
        fields = (
            'assigned_date',
            'shipment_cost',
            'comment',
        )
