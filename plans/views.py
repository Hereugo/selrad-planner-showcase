from django.shortcuts import render, redirect
from django.core.paginator import Paginator

from .models import Plan
from .forms import PlanForm
from clients.models import Client
from managers.models import Manager


def index(request):
    if request.method == 'POST':
        print(request.POST)
        form = PlanForm(request.POST)
        if form.is_valid():
            plan = form.save(commit=False)
            client = Client.objects.get(pk=request.POST['client'])
            # managers = Manager.objects.filter(pk__in=request.POST.getlist('managers'))

            plan.client = client
            # plan.managers.set(managers)

            plan.save()
            form.save_m2m()

        return redirect('index')
    else:
        plans = Plan.objects.all()
        paginator = Paginator(plans, 10)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        clients = Client.objects.all()
        managers = Manager.objects.all()
        worklist = Plan.WORKLIST

        return render(request, 'index.html', {'page_obj': page_obj, 'clients': clients, 'managers': managers, 'worklist': worklist})
