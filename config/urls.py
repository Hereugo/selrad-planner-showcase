from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from plans.views import PlanListView, PlanCreateView, plan_show_modal, index

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', index, name='index'),
    path('plans', PlanListView.as_view(), name='plans'),
    path('plans/create', PlanCreateView.as_view(), name='plan_create'),
    path('plans/modal', plan_show_modal, name='plan_show_modal_default'),
    path('plans/modal/<uuid:pk>', plan_show_modal, name='plan_show_modal'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
