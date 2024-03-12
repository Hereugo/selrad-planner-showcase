import re
from django.views.generic import ListView, CreateView
from django.shortcuts import render, redirect

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
    filterset_class = PlanFilter
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # remove 'page' from GET parameters, so we can keep the search parameters. 
        context['urlencode'] = re.split(r'page=\d+', self.request.GET.urlencode())[-1][1:]

        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = self.filterset_class(self.request.GET, queryset=queryset).qs
        return queryset


def plan_create(request, pk=None):
    if request.method == 'POST':
        form = PlanForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('plans', request)

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
