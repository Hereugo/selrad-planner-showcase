from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from plans.views import PlanListView, plan_create, index



urlpatterns = [
    path('admin/', admin.site.urls),

    path('', index, name='index'),
    path('plans', PlanListView.as_view(), name='plans'),
    
    path('plans/create', plan_create, name='plan_create_default'),
    path('plans/create/<uuid:pk>', plan_create, name='plan_create'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
