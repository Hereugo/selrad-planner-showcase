import logging

from django.db.models import F, ExpressionWrapper, DurationField
from django.utils import timezone
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.schemas.openapi import AutoSchema
from drf_spectacular.utils import extend_schema, OpenApiParameter

from plans.models import Plan, Worklist
from managers.models import Manager

from api.utils.custom_permissions import (
    IsAuthenticated,
    HasCRUDPermission,
    permission_required,
)
from api.utils.custom_paginations import PageLimitPagination
from .serializers import (
    PlanSerializer,
    PlanUpdateSerializer,
    WorklistSerializer,
)
from .custom_permissions import CanChangeFuturePlans, CanDeleteFuturePlans
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

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        if self.action in ("update", "partial_update"):
            permission_classes.append(CanChangeFuturePlans)
        elif self.action == "destroy":
            permission_classes.append(CanDeleteFuturePlans)

        permission_classes.append(HasCRUDPermission)

        logger.debug(f"Permission classes: {permission_classes}")

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return PlanUpdateSerializer

        return super().get_serializer_class()

    @extend_schema(
        methods=["get"],
        description="Скачать план",
        filters=True,
    )
    @action(
        detail=False,
        methods=["get"],
        permission_classes=[IsAuthenticated],
        url_path="export",
    )
    @permission_required("plans.export_plans")
    def export(self, request, plans=None):
        """Скачать план."""

        plans = self.filter_queryset(plans or self.get_queryset())

        if plans.count() == 0:
            return Response(
                {"error": "Нет планов для выбранных фильтров."},
                status=status.HTTP_404_NOT_FOUND,
            )

        logger.info("GET: ", request.GET)

        # get date_before and date_after from filters
        date_before = request.GET.get("date_before", None)
        date_after = request.GET.get("date_after", None)

        if not date_before:
            date_before = plans.latest("assigned_date").assigned_date
        else:
            date_before = timezone.datetime.strptime(date_before, "%Y-%m-%d")

        if not date_after:
            date_after = plans.earliest("assigned_date").assigned_date
        else:
            date_after = timezone.datetime.strptime(date_after, "%Y-%m-%d")

        buffer = generate_excelsheet_by_plan(plans, date_after, date_before)

        filename = f"ПЛАНЫ С {date_after.strftime('%d-%m-%Y')} ПО {date_before.strftime('%d-%m-%Y')}.xlsx"

        response = HttpResponse(
            buffer.getvalue(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Access-Control-Expose-Headers"] = "Content-Disposition"
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        return response

    @extend_schema(
        methods=["get"],
        description="Скачать отчет менеджера",
        filters=True,
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
    @permission_required("plans.export_report")
    def export_report(self, request, manager_id=None, plans=None):
        """Скачать отчет."""
        manager = get_object_or_404(Manager, pk=manager_id)

        # Method export report is used here, because filters are applied here.
        plans = self.filter_queryset(plans or self.get_queryset())
        plans = plans.filter(managers__id=manager_id)

        if plans.count() == 0:
            return Response(
                {"error": "Нет планов для выбранных фильтров."},
                status=status.HTTP_404_NOT_FOUND,
            )

        logger.info("GET: ", request.GET)

        # get date_before and date_after from filters
        date_before = request.GET.get("date_before", None)
        date_after = request.GET.get("date_after", None)

        if not date_before:
            date_before = plans.latest("assigned_date").assigned_date
        else:
            date_before = timezone.datetime.strptime(date_before, "%Y-%m-%d")

        if not date_after:
            date_after = plans.earliest("assigned_date").assigned_date
        else:
            date_after = timezone.datetime.strptime(date_after, "%Y-%m-%d")

        buffer = generate_excelsheet_by_manager(plans, manager, date_after, date_before)

        filename = f"ОТЧЕТ {manager} С {date_after.strftime('%d-%m-%Y')} ПО {date_before.strftime('%d-%m-%Y')}.xlsx"

        response = HttpResponse(
            buffer.getvalue(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        response["Access-Control-Expose-Headers"] = "Content-Disposition"
        return response


class WorklistViewSet(ReadOnlyModelViewSet):
    """API для работы с рабочими списками."""

    queryset = Worklist.objects.all()
    serializer_class = WorklistSerializer
    pagiation_class = None
