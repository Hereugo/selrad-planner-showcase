import logging

from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.schemas.openapi import AutoSchema
from drf_spectacular.utils import extend_schema, OpenApiParameter
from django.http import HttpResponse

from plans.models import Plan, Worklist

from api.utils.custom_permissions import IsAuthenticated
from api.utils.custom_paginations import PageLimitPagination
from .serializers import (
    PlanSerializer,
    PlanUpdateSerializer,
    WorklistSerializer,
    MapSerializer,
)
from .custom_filters import PlanFilter
from .generate_excelsheet import (
    generate_excelsheet_by_plan,
    generate_excelsheet_by_manager,
)


logger = logging.getLogger(__name__)


class PlanViewSet(ModelViewSet):
    """API для работы с планами."""

    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    pagination_class = PageLimitPagination
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    filterset_class = PlanFilter
    search_fields = (
        "client__name",
        "managers__first_name",
        "worklist__name",
    )

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return PlanUpdateSerializer

        return super().get_serializer_class()

    @extend_schema(methods=["get"], description="Скачать план", filters=True)
    @action(
        detail=False,
        methods=["get"],
        permission_classes=[IsAuthenticated],
        url_path="export",
    )
    def export(self, request, plans=None):
        """Скачать план."""

        if not plans:
            plans = self.filter_queryset(self.get_queryset())

        buffer = generate_excelsheet_by_plan(plans)

        # TODO: Add from what daterange
        filename = "планы.xlsx"

        response = HttpResponse(
            buffer.getvalue(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        return response

    @extend_schema(
        methods=["get"],
        description="Скачать отчет менеджера",
        parameters=[
            OpenApiParameter(
                "manager_id",
                str,
                OpenApiParameter.PATH,
                description="id менеджера",
                required=True,
            )
        ],
    )
    @action(
        detail=False,
        methods=["get"],
        permission_classes=[IsAuthenticated],
        url_path=r"export_report/(?P<manager_id>\d+)",
    )
    def export_report(self, request, manager_id=None, plans=None):
        """Скачать отчет."""
        # Method export report is used here, because filters are applied here.
        if not plans:
            plans = self.filter_queryset(self.get_queryset())
        manager = get_object_or_404(Manager, pk=manager_id)

        buffer = generate_excelsheet_by_manager(plans, manager)

        # TODO: Add from what daterange
        filename = "отчет.xlsx"

        response = HttpResponse(
            buffer.getvalue(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        return response


class WorklistViewSet(ReadOnlyModelViewSet):
    """API для работы с рабочими списками."""

    queryset = Worklist.objects.all()
    serializer_class = WorklistSerializer
    pagiation_class = None
