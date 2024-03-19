from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from plans.views import PlanListView, plan_create, index, plans_excel, plan_show_map, plan_delete, aside_buttons, get_client_address


urlpatterns = [
    path('admin/', admin.site.urls),

    path('aside_buttons/', aside_buttons, name='aside_buttons'),

    path('', index, name='index'),
    path('plans', PlanListView.as_view(), name='plans'),

    path('plans/create', plan_create, name='plan_create_default'),
    path('plans/create/<uuid:pk>', plan_create, name='plan_create'),
    path('client_address/', get_client_address, name='client_address'),

    path('plans/show_map', plan_show_map, name='plan_show_map_default'),
    path('plans/show_map/<uuid:pk>', plan_show_map, name='plan_show_map'),

    path('plans/excel', plans_excel, name='plans_excel')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
