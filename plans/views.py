from django.views.generic import ListView, CreateView
from django.shortcuts import render

from .filters import PlanFilter
from .forms import PlanForm
from .models import Plan, Worklist

from clients.models import Client 
from managers.models import Manager


def index(request):
    return render(request, 'index.html')


class PlanListView(ListView):
    model = Plan 
    template_name = 'plans.html'
    queryset = Plan.objects.all()
    paginate_by = 10
    filterset_class = PlanFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = self.filterset_class(self.request.GET, queryset=queryset).qs

        return queryset


def plan_show_modal(request, pk=None):
    plan = Plan.objects.filter(pk=pk).first()
    clients = Client.objects.all()
    worklist = Worklist.objects.all()
    managers = Manager.objects.all()

    return render(request, 'plan_modal_form.html', {
        'plan': plan,
        'clients': clients,
        'worklist': worklist,
        'managers': managers
    })


class PlanCreateView(CreateView):
    form_class = PlanForm
    model = Plan 
    queryset = Plan.objects.all()
    paginate_by = 10
    filterset_class = PlanFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = self.filterset_class(self.request.GET, queryset=queryset).qs

        return queryset