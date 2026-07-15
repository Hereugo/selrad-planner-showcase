from django.urls import path

from api.v1.manager_scores.views import ManagerScoresView

urlpatterns = [
    path("manager_scores/", ManagerScoresView.as_view(), name="manager-scores"),
]
