import logging
from datetime import datetime
from typing import Optional, cast

from api.plans.custom_mixins import (
    BaseFilterSerializer,
    CompareYearsFilterSerializer,
    DispatchListFilterSerializer,
    ReportFilterSerializer,
)
from api.utils.custom_paginations import PageLimitPagination
from api.utils.custom_permissions import (
    HasCRUDPermission,
    IsAuthenticated,
    permission_required,
)
from dateutil.relativedelta import relativedelta
from django.db.models import QuerySet
from django.http import HttpResponse
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from managers.models import Manager
from plans.models import PaymentRegistry, Plan, PlanWorkItem, WorkItem
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet, ReadOnlyModelViewSet

from .custom_filters import PaymentRegistryFilter, PlanFilter, TaskFilter
from .custom_permissions import CanDeleteFuturePlans
from .custom_schemas import *
from .generate_compare_years import generate_compare_years
from .generate_dispatch_list import generate_dispatch_list
from .generate_dispatch_report import generate_dispatch_report
from .generate_excelsheet import (
    generate_excelsheet_by_manager,
    generate_excelsheet_by_plan,
)
from .serializers import (
    PaymentRegistrySerializer,
    PaymentRegistryUpdateSerializer,
    PlanCreateSerializer,
    PlanSerializer,
    PlanUpdateSerializer,
    WorkItemSerializer,
)
from .work_items_serializers import TaskSerializer, TaskUpdatePolymorphicSerializer

logger = logging.getLogger(__name__)


class PlanViewSet(ModelViewSet):
    """API для работы с планами."""

    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    pagination_class = PageLimitPagination
    permission_classes = [IsAuthenticated, HasCRUDPermission]
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    filterset_class = PlanFilter
    search_fields = (
        "client__name",
        "managers__name",
        "work_items__name",
    )

    def get_permissions(self):
        permission_classes = self.permission_classes

        if self.action == "destroy":
            permission_classes.append(CanDeleteFuturePlans)

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action in ("create",):
            return PlanCreateSerializer
        if self.action in ("update", "partial_update"):
            return PlanUpdateSerializer

        return super().get_serializer_class()

    @export_schema(
        parameters=[CompareYearsFilterSerializer],
        responses=DEFAULT_EXCEL_RESPONSE,
        summary="Скачать сравнить по периодам",
    )
    @action(
        detail=False,
        methods=["get"],
        permission_classes=[IsAuthenticated],
        url_path=r"export_compare_years",
    )
    @permission_required("clients.export_compare_years")
    def export_compare_years(self, request: Request) -> HttpResponse:
        """Скачать сравнить по периодам."""

        filter_serializer = CompareYearsFilterSerializer(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)

        logger.info(filter_serializer.validated_data)

        start_date: datetime = filter_serializer.validated_data["start_date"]
        end_date: datetime = filter_serializer.validated_data["end_date"]
        to_year_diff: int = filter_serializer.validated_data["to_year_diff"]

        period_2 = {
            "start_date": start_date,
            "end_date": end_date,
        }
        period_1 = period_2.copy()

        period_1["start_date"] = period_2["start_date"] - relativedelta(
            years=to_year_diff
        )
        period_1["end_date"] = period_2["end_date"] - relativedelta(years=to_year_diff)

        buffer = generate_compare_years(period_1, period_2, request)

        filename = f"СРАВНИТЬ {period_1['start_date'].strftime('%d-%m-%Y')} ПО {period_1['end_date'].strftime('%d-%m-%Y')} ПРОТИВ {period_2['start_date'].strftime('%d-%m-%Y')} ПО {period_2['end_date'].strftime('%d-%m-%Y')} ГОДА.xlsx"

        response = HttpResponse(
            buffer.getvalue(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Access-Control-Expose-Headers"] = "Content-Disposition"
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        return response

    @export_schema(
        parameters=[DispatchListFilterSerializer],
        # responses=DEFAULT_IMG_RESPONSE,
        summary="Получить диспетчерский лист",
    )
    @action(
        detail=False,
        methods=["get"],
        permission_classes=[IsAuthenticated],
        url_path="dispatch_list",
    )
    @permission_required("plans.get_dispatch_list")
    def dispatch_list(self, request):
        filter_serializer = DispatchListFilterSerializer(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)

        logger.info(filter_serializer.validated_data)

        start_date: Optional[datetime] = filter_serializer.validated_data["start_date"]
        end_date: Optional[datetime] = filter_serializer.validated_data["end_date"]
        comment: str = filter_serializer.validated_data["comment"]
        manager: Manager = filter_serializer.validated_data["manager"]

        plans: QuerySet[Plan] = self.filter_queryset(self.get_queryset())
        plans = plans.filter(managers=manager)
        plans = plans.order_by("assigned_date")

        if filter_serializer.validated_data["set_time_dispatch"]:
            plans.filter(time_since_first_dispatch__isnull=True).update(
                time_since_first_dispatch=timezone.now()
            )

        if not start_date:
            start_date = cast(datetime, plans.earliest("assigned_date").assigned_date)
        if not end_date:
            end_date = cast(datetime, plans.latest("assigned_date").assigned_date)

        buffer = generate_dispatch_list(plans, manager, comment, start_date, end_date)
        filename: str = (
            f"ДИСПЕТЧЕРСКИЙ ЛИСТ {manager.name} С {end_date.strftime('%d-%m-%Y')} ПО {start_date.strftime('%d-%m-%Y')}.png"
        )

        response = HttpResponse(
            buffer.getvalue(),
            content_type="image/png",
        )
        response["Access-Control-Expose-Headers"] = "Content-Disposition"
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        return response

    @export_schema(
        parameters=[BaseFilterSerializer],
        responses=DEFAULT_EXCEL_RESPONSE,
        summary="Cкачать диспетчерский отчет по периоду",
    )
    @action(
        detail=False,
        methods=["get"],
        permission_classes=[IsAuthenticated],
        url_path="dispatch_report",
    )
    @permission_required("plans.get_dispatch_report")
    def dispatch_report(self, request):
        """Cкачать диспетчерский отчет по периоду"""

        filter_serializer = BaseFilterSerializer(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)

        start_date: Optional[datetime] = filter_serializer.validated_data["start_date"]
        end_date: Optional[datetime] = filter_serializer.validated_data["end_date"]

        plans = self.filter_queryset(self.get_queryset())
        plans = plans.order_by("assigned_date")

        if not start_date:
            start_date = cast(datetime, plans.earliest("assigned_date").assigned_date)
        if not end_date:
            end_date = cast(datetime, plans.latest("assigned_date").assigned_date)

        work_items_shipments = (
            PlanWorkItem.objects.filter(plan__in=plans, content_type__model="shipment")
            .prefetch_related("content_object")
            .select_related("plan")
        )

        buffer = generate_dispatch_report(work_items_shipments, start_date, end_date)

        filename = f"ОТЧЕТ ПО ДИСПЕЧЕРСКОМУ С {start_date.strftime('%d-%m-%Y')} ПО {end_date.strftime('%d-%m-%Y')}.xlsx"

        response = HttpResponse(
            buffer.getvalue(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Access-Control-Expose-Headers"] = "Content-Disposition"
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        return response

    @export_schema(
        parameters=[BaseFilterSerializer],
        responses=DEFAULT_EXCEL_RESPONSE,
        summary="Скачать план",
    )
    @action(
        detail=False,
        methods=["get"],
        permission_classes=[IsAuthenticated],
        url_path="export",
    )
    @permission_required("plans.export_plans")
    def export(self, request):
        """Скачать план."""

        filter_serializer = BaseFilterSerializer(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)

        start_date: Optional[datetime] = filter_serializer.validated_data["start_date"]
        end_date: Optional[datetime] = filter_serializer.validated_data["end_date"]

        plans = self.filter_queryset(self.get_queryset())
        plans = plans.order_by("assigned_date")

        if not start_date:
            start_date = cast(datetime, plans.earliest("assigned_date").assigned_date)
        if not end_date:
            end_date = cast(datetime, plans.latest("assigned_date").assigned_date)

        buffer = generate_excelsheet_by_plan(plans, start_date, end_date)

        filename = f"ПЛАНЫ С {start_date.strftime('%d-%m-%Y')} ПО {end_date.strftime('%d-%m-%Y')}.xlsx"

        response = HttpResponse(
            buffer.getvalue(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Access-Control-Expose-Headers"] = "Content-Disposition"
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        return response

    @export_schema(
        parameters=[ReportFilterSerializer],
        responses=DEFAULT_EXCEL_RESPONSE,
        summary="Скачать отчет менеджера",
    )
    @action(
        detail=False,
        methods=["get"],
        permission_classes=[IsAuthenticated],
        url_path=r"export_report",
    )
    @permission_required("plans.export_report")
    def export_report(self, request):
        """Скачать отчет."""

        filter_serializer = ReportFilterSerializer(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)

        start_date: Optional[datetime] = filter_serializer.validated_data["start_date"]
        end_date: Optional[datetime] = filter_serializer.validated_data["end_date"]
        manager: Manager = filter_serializer.validated_data["manager"]

        # Method export report is used here, because filters are applied here.
        plans = self.filter_queryset(self.get_queryset())
        plans = plans.filter(managers=manager)
        plans = plans.order_by("assigned_date")

        if not start_date:
            start_date = cast(datetime, plans.earliest("assigned_date").assigned_date)
        if not end_date:
            end_date = cast(datetime, plans.latest("assigned_date").assigned_date)

        buffer = generate_excelsheet_by_manager(plans, manager, start_date, end_date)

        filename = f"ОТЧЕТ {manager.name} С {start_date.strftime('%d-%m-%Y')} ПО {end_date.strftime('%d-%m-%Y')}.xlsx"

        response = HttpResponse(
            buffer.getvalue(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        response["Access-Control-Expose-Headers"] = "Content-Disposition"
        return response


class WorkItemViewSet(ReadOnlyModelViewSet):
    """API для работы с рабочими списками."""

    queryset = WorkItem.objects.all()
    serializer_class = WorkItemSerializer
    pagination_class = None


@extend_schema_view(
    update=extend_schema(
        request=TaskUpdatePolymorphicSerializer,
        responses=TaskSerializer,
    ),
    partial_update=extend_schema(
        request=TaskUpdatePolymorphicSerializer,
        responses=TaskSerializer,
    ),
)
class TaskViewSet(ListModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    """API для работы с задачами."""

    # Показывать только задачи с отгрузками
    queryset = PlanWorkItem.objects.filter(
        work_item__content_type__model__in=("shipment",)
    )
    serializer_class = TaskSerializer
    filterset_class = TaskFilter
    pagination_class = PageLimitPagination

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(plan__managers__user=self.request.user)

    def update(self, request, *args, **kwargs):
        task_instance: PlanWorkItem = self.get_object()

        work_item_serializer = TaskUpdatePolymorphicSerializer(
            task_instance.content_object,
            data=request.data,
            context={"request": request},
        )
        work_item_serializer.is_valid(raise_exception=True)
        work_item_serializer.save()

        task_serializer = TaskSerializer(task_instance)

        return Response(task_serializer.data)


# Permission to view: read_payment_registries
class PaymentRegistryViewSet(
    ListModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet
):
    queryset = PaymentRegistry.objects.all()
    serializer_class = PaymentRegistrySerializer
    # pagination_class = PageLimitPagination
    permission_classes = [
        IsAuthenticated,
        HasCRUDPermission,
    ]
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    filterset_class = PaymentRegistryFilter

    def get_queryset(self):
        qs = super().get_queryset()
        return qs | PaymentRegistry.objects.filter(is_confirmed=False)

    def get_serializer_class(self):
        if self.action in ("update", "partial_update"):
            return PaymentRegistryUpdateSerializer

        return super().get_serializer_class()
