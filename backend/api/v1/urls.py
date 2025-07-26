from django.urls import include, path

urlpatterns = [
    path("", include("api.v1.clients.urls")),
    path("", include("api.v1.plans.urls")),
    path("", include("api.v1.users.urls")),
    path("", include("api.v1.exports.urls")),
]
