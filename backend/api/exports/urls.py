from django.urls import path

from .plans import export

urlpatterns = [path("plans", export)]
