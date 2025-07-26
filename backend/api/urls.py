from django.conf import settings
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

app_name = "api"

urlpatterns = [
    path("auth/", include("djoser.urls.jwt")),
    path("v1/", include("api.clients.urls")),
    path("v1/", include("api.plans.urls")),
    path("v1/", include("api.users.urls")),
    path("v1/", include("api.exports.urls")),
]

if settings.DEBUG:
    urlpatterns += [
        path("schema/", SpectacularAPIView.as_view(), name="schema"),
        path(
            "schema/swagger-ui/",
            SpectacularSwaggerView.as_view(url_name="api:schema"),
            name="swagger-ui",
        ),
        path(
            "schema/redoc/",
            SpectacularRedocView.as_view(url_name="api:schema"),
            name="redoc",
        ),
    ]
