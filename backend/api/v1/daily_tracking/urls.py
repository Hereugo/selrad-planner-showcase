from django.urls import path

from api.v1.daily_tracking.views import DailyTrackingView

urlpatterns = [
    path("daily_tracking", DailyTrackingView.as_view(), name="daily-tracking"),
]
