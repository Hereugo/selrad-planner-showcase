from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from plans.views import index, get_plan, create_plan

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', index, name='index'),
    path('plans/<uuid:pk>', get_plan, name='get_plan'),
    path('plans/create', create_plan, name='create_plan')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
