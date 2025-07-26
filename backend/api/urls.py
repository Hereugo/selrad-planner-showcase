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
    path("v1/", include("api.v1.urls")),
    path("v2/", include("api.v2.urls")),
]

if settings.DEBUG:
    urlpatterns += [
        path(
            "schema/v1/",
            SpectacularAPIView.as_view(
                patterns=[
                    path("api/auth/", include("djoser.urls.jwt")),
                    path("api/v1/", include("api.v1.urls")),
                ],
            ),
            name="schema-v1",
        ),
        path("docs/v1/", SpectacularSwaggerView.as_view(url_name="api:schema-v1")),
        path(
            "schema/v2/",
            SpectacularAPIView.as_view(
                patterns=[
                    path("api/auth/", include("djoser.urls.jwt")),
                    path("api/v2/", include("api.v2.urls")),
                ],
            ),
            name="schema-v2",
        ),
        path("docs/v2/", SpectacularSwaggerView.as_view(url_name="api:schema-v2")),
    ]

    # urlpatterns += [
    #     path("schema/", SpectacularAPIView.as_view(), name="schema"),
    #     path(
    #         "schema/swagger-ui/",
    #         SpectacularSwaggerView.as_view(url_name="api:schema"),
    #         name="swagger-ui",
    #     ),
    #     path(
    #         "schema/redoc/",
    #         SpectacularRedocView.as_view(url_name="api:schema"),
    #         name="redoc",
    #     ),
    # ]
