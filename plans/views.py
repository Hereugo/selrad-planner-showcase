from django.shortcuts import render
from django.core.paginator import Paginator

from .models import Plan


def index(request):
    plans = Plan.objects.all()
    paginator = Paginator(plans, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    print(page_obj.paginator.count)

    return render(request, 'index.html', {'page_obj': page_obj})
