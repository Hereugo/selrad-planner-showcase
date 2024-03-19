from django import forms
from .models import Plan, Worklist
from managers.models import Manager
from clients.models import Client, Address

from utils.m2m import m2m_create, m2m_update

class PlanForm(forms.ModelForm):
    class Meta:
        model = Plan
        fields = (
            'assigned_date',
            'shipment_cost',
            'comment',
        )

    def save(self, commit=True):
        worklist_ids = [k.split('_')[1] for k, _ in self.data.items() if 'worklist' in k]
        manager_ids = [k.split('_')[1] for k, _ in self.data.items() if 'manager' in k]
        client_id = self.data['client']
        address_id = self.data['address']

        self.cleaned_data['worklist'] = [Worklist.objects.get(pk=worklist_id) for worklist_id in worklist_ids]
        self.cleaned_data['managers'] = [Manager.objects.get(pk=manager_id) for manager_id in manager_ids]
        self.cleaned_data['client'] = Client.objects.get(pk=client_id)
        self.cleaned_data['address'] = Address.objects.get(pk=address_id)
    
        if self.data.get('uuid'):
            plan = Plan.objects.get(pk=self.data['uuid'])
            m2m_update(plan, self.cleaned_data)
        else:
            plan = m2m_create(Plan, self.cleaned_data)

        return plan
