from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse

from datetime import datetime

from utils import model_meta

from .models import Plan, PlanManager, Worklist, PlanWorklist
from .forms import PlanForm
from clients.models import Client
from managers.models import Manager


def m2m_create(ModelClass, validated_data):
    info = model_meta.get_field_info(ModelClass)

    many_to_many = {}
    for field_name, relation_info in info.relations.items():
        print(field_name, relation_info.to_many)

        if relation_info.to_many and (field_name in validated_data):
            many_to_many[field_name] = validated_data.pop(field_name)

    instance = ModelClass._default_manager.create(**validated_data)

    if many_to_many:
        for field_name, value in many_to_many.items():
            field = getattr(instance, field_name)
            field.set(value)

    return instance


def m2m_update(instance, validated_data):
    info = model_meta.get_field_info(instance)

    m2m_fields = []
    for attr, value in validated_data.items():
        if attr in info.relations and info.relations[attr].to_many:
            m2m_fields.append((attr, value))
        else:
            setattr(instance, attr, value)

    instance.save()

    for attr, value in m2m_fields:
        field = getattr(instance, attr)
        field.set(value)

    return instance


def index(request):
    plans = Plan.objects.all()
    paginator = Paginator(plans, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    clients = Client.objects.all()
    managers = Manager.objects.all()
    worklist = Worklist.objects.all()

    return render(request, 'index.html', {'page_obj': page_obj, 'clients': clients, 'managers': managers, 'worklist': worklist})


def get_plan(request, pk):
    plan = get_object_or_404(Plan, pk=pk)
    return JsonResponse({
        'uuid': plan.pk,
        'shipment_cost': float(plan.shipment_cost),
        'assigned_date': plan.assigned_date.strftime('%m/%d/%Y'),
        'comment': plan.comment,
        'client': plan.client.id,
        'managers': [manager.id for manager in plan.managers.all()],
        'worklist': [worklist.id for worklist in plan.worklist.all()],
        'created_at': plan.created_at,
        'updated_at': plan.updated_at
    })


def create_plan(request):
    if request.method == 'POST':
        uuid = request.POST.get('uuid') or None
        plan = Plan.objects.get(pk=uuid) if uuid else None

        worklist_ids = [ int(k.split('_')[1]) for k, _ in request.POST.items() if "worklist" in k]
        manager_ids = [ int(k.split('_')[1]) for k, _ in request.POST.items() if "manager" in k]

        form = PlanForm(request.POST)
        if form.is_valid():
            validated_data = form.cleaned_data.copy()
            validated_data['worklist'] = [Worklist.objects.get(pk=worklist_id) for worklist_id in worklist_ids]
            validated_data['managers'] = [Manager.objects.get(pk=manager_id) for manager_id in manager_ids]
            validated_data['client'] = Client.objects.get(pk=request.POST['client'])

            if plan:
                m2m_update(plan, validated_data)
            else: 
                m2m_create(Plan, validated_data)

        # TODO: Redirect to index with success message if the form is valid
        return redirect('index')
