import logging

from django.db.models import F, ExpressionWrapper, DurationField
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
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
from clients.models import Client
from managers.models import Manager

from api.utils.custom_permissions import IsAuthenticated
from api.utils.custom_paginations import PageLimitPagination
from api.clients.serializers import NearbyClientSerializer
from .serializers import (
    PlanSerializer,
    PlanUpdateSerializer,
    WorklistSerializer,
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
    def export(self, request, plans=None):
        """Скачать план."""

        if not plans:
            plans = self.filter_queryset(self.get_queryset())

        if plans.count() == 0:
            return Response(
                {"error": "Нет планов для выбранных фильтров."},
                status=status.HTTP_404_NOT_FOUND,
            )

        buffer = generate_excelsheet_by_plan(plans)

        earliest_date = plans.earliest("assigned_date").assigned_date.strftime(
            "%d-%m-%Y"
        )
        latest_date = plans.latest("assigned_date").assigned_date.strftime("%d-%m-%Y")
        filename = f"ПЛАНЫ С {earliest_date} ПО {latest_date}.xlsx"

        response = HttpResponse(
            buffer.getvalue(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
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
    def export_report(self, request, manager_id=None, plans=None):
        """Скачать отчет."""
        # Method export report is used here, because filters are applied here.
        if not plans:
            plans = self.filter_queryset(self.get_queryset())
        else:
            plans = self.filter_queryset(plans)

        manager = get_object_or_404(Manager, pk=manager_id)

        plans = plans.filter(managers=manager)

        if plans.count() == 0:
            return Response(
                {"error": "Нет планов для выбранных фильтров."},
                status=status.HTTP_404_NOT_FOUND,
            )

        buffer = generate_excelsheet_by_manager(plans, manager)

        earliest_date = plans.earliest("assigned_date").assigned_date.strftime(
            "%d-%m-%Y"
        )
        latest_date = plans.latest("assigned_date").assigned_date.strftime("%d-%m-%Y")
        filename = f"ОТЧЕТ {manager} С {earliest_date} ПО {latest_date}.xlsx"

        response = HttpResponse(
            buffer.getvalue(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        return response

    @extend_schema(
        methods=["get"],
        parameters=[
            OpenApiParameter(
                "radius",
                float,
                OpenApiParameter.QUERY,
                description="Радиус поиска в км",
                default=0.5,
            ),
            OpenApiParameter(
                "time_threshold",
                int,
                OpenApiParameter.QUERY,
                description="Порог времени в днях",
                default=30,
            ),
        ],
        responses={200: NearbyClientSerializer(many=True)},
    )
    @action(
        detail=True,
        methods=["get"],
        permission_classes=[IsAuthenticated],
        url_path="find_nearby",
    )
    def find_nearby(self, request, pk=None):
        """Найти ближайшие планы по текущему плану."""
        plan = get_object_or_404(Plan, pk=pk)
        radius = float(request.GET.get("radius", 0.5))
        time_threshold = int(request.GET.get("time_threshold", 30))

        # get all clients that are in the radius of a circle [plan.client.address.point, radius]
        nearby_clients = Client.objects.filter(
            address__point__distance_lte=(
                plan.client.address.point,
                Distance(km=radius),
            )
        ).exclude(pk=plan.client.pk)

        # get all clients that have plans in the time range [assigned_date - time_threshold, assigned_date]
        a = nearby_clients.filter(
            plans__assigned_date__gte=plan.assigned_date
            - timezone.timedelta(days=time_threshold),
            plans__assigned_date__lte=plan.assigned_date,
        )
        # get all clients that have no plans
        b = nearby_clients.filter(plans__isnull=True)
        nearby_clinets = a | b

        # remove all duplicates
        nearby_clients = nearby_clients.distinct()

        serializer = NearbyClientSerializer(
            nearby_clients, many=True, context={"request": request, "plan_pk": pk}
        )
        return Response(serializer.data)


class WorklistViewSet(ReadOnlyModelViewSet):
    """API для работы с рабочими списками."""

    queryset = Worklist.objects.all()
    serializer_class = WorklistSerializer
    pagiation_class = None
