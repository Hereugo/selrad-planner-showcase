import logging

from datetime import datetime
from django.utils import timezone
from django.http import HttpResponse
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.types import OpenApiTypes
from rest_framework import filters, status
from rest_framework.permissions import BasePermission
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet, GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from drf_spectacular.utils import (
    OpenApiResponse,
    extend_schema,
    OpenApiParameter,
    extend_schema_view,
)

from plans.models import Plan, WorkItem, PlanWorkItem
from managers.models import Manager

from api.utils.custom_permissions import (
    IsAuthenticated,
    HasCRUDPermission,
    permission_required,
)
from api.utils.custom_paginations import PageLimitPagination
from .serializers import (
    PlanCreateSerializer,
    PlanSerializer,
    PlanUpdateSerializer,
    WorkItemSerializer,
)
from .work_items_serializers import TaskSerializer, TaskUpdatePolymorphicSerializer

from .custom_permissions import (
    # CanAddFuturePlans,
    # CanChangeFuturePlans,
    CanDeleteFuturePlans,
)
from .custom_filters import PlanFilter, TaskFilter
from .generate_compare_years import generate_compare_years
from .generate_dispatch_report import generate_dispatch_report
from .generate_dispatch_list import generate_dispatch_list
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
        "managers__name",
        "work_items__name",
    )

    def get_permissions(self):
        permission_classes: list[type[BasePermission]] = [IsAuthenticated]
        # if self.action in ("update", "partial_update"):
        #     permission_classes.append(CanChangeFuturePlans)
        if self.action == "destroy":
            permission_classes.append(CanDeleteFuturePlans)

        permission_classes.append(HasCRUDPermission)

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action in ("create",):
            return PlanCreateSerializer
        if self.action in ("update", "partial_update"):
            return PlanUpdateSerializer

        return super().get_serializer_class()

    @extend_schema(
        methods=["get"],
        description="Скачать сравнить по периодам",
        filters=True,
        summary="Скачать сравнить по периодам",
        parameters=[
            OpenApiParameter(
                "to_year_diff",
                int,
                description="Сравнить с каким годом (differance)",
                default=1,
            ),
        ],
    )
    @action(
        detail=False,
        methods=["get"],
        permission_classes=[IsAuthenticated],
        url_path=r"export_compare_years",
    )
    @permission_required("clients.export_compare_years")
    def export_compare_years(self, request):
        """Скачать сравнить по периодам."""

        start_date = request.query_params.get("start_date", None)
        end_date = request.query_params.get("end_date", None)
        to_year_diff = int(request.query_params.get("to_year_diff", 1))

        if not start_date or not end_date:
            return Response(
                {"error": "Выберите период"},
                status=status.HTTP_404_NOT_FOUND,
            )

        if to_year_diff < 0:
            return Response(
                {"error": "Против год не может быть отрицательным"},
                status=status.HTTP_404_NOT_FOUND,
            )

        period_2 = {
            "start_date": datetime.strptime(start_date, "%Y-%m-%d"),
            "end_date": datetime.strptime(end_date, "%Y-%m-%d"),
        }
        period_1 = period_2.copy()
        period_1["start_date"] = period_1["start_date"].replace(
            year=period_1["start_date"].year - to_year_diff
        )
        period_1["end_date"] = period_1["end_date"].replace(
            year=period_1["end_date"].year - to_year_diff
        )

        buffer = generate_compare_years(period_1, period_2, request)

        filename = f"СРАВНИТЬ {period_1['start_date'].strftime('%d-%m-%Y')} ПО {period_1['end_date'].strftime('%d-%m-%Y')} ПРОТИВ {period_2['start_date'].strftime('%d-%m-%Y')} ПО {period_2['end_date'].strftime('%d-%m-%Y')} ГОДА.xlsx"

        response = HttpResponse(
            buffer.getvalue(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Access-Control-Expose-Headers"] = "Content-Disposition"
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        return response

    @extend_schema(
        methods=["get"],
        description="Получить диспетчерский лист",
        summary="Получить диспетчерский лист",
        filters=True,
        parameters=[
            OpenApiParameter(
                "comment",
                str,
                description="Комментарий",
            ),
            OpenApiParameter(
                "manager_id",
                str,
                OpenApiParameter.PATH,
                description="id менеджера",
                required=True,
            ),
        ],
        responses={
            (200, "image/png"): OpenApiResponse(
                response=OpenApiTypes.BYTE,
                description="Диспетчерский лист",
            )
        },
    )
    @action(
        detail=False,
        methods=["get"],
        permission_classes=[IsAuthenticated],
        url_path="dispatch_list/(?P<manager_id>\d+)",
    )
    @permission_required("plans.get_dispatch_list")
    def dispatch_list(self, request, manager_id=None):
        start_date = request.query_params.get("start_date", None)
        end_date = request.query_params.get("end_date", None)
        comment = request.query_params.get("comment", "")

        manager: Manager = get_object_or_404(Manager, id=manager_id)

        # If manager is not a driver, then he can't get dispatch list.
        if not manager.is_driver:
            return Response(
                {"error": "Менеджер не является водителем."},
                status=status.HTTP_403_FORBIDDEN,
            )

        plans: QuerySet[Plan] = self.filter_queryset(self.get_queryset())
        plans = plans.filter(managers__id=manager_id)
        plans = plans.order_by("assigned_date")

        plans.filter(time_since_first_dispatch__isnull=True).update(
            time_since_first_dispatch=timezone.now()
        )

        if not start_date:
            start_date = plans.earliest("assigned_date").assigned_date
        else:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")

        if not end_date:
            end_date = plans.latest("assigned_date").assigned_date
        else:
            end_date = datetime.strptime(end_date, "%Y-%m-%d")

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

    @extend_schema(
        methods=["get"],
        description="Cкачать диспетчерский отчет по периоду",
        filters=True,
        summary="Cкачать диспетчерский отчет по периоду",
    )
    @action(
        detail=False,
        methods=["get"],
        permission_classes=[IsAuthenticated],
        url_path="dispatch_report",
    )
    @permission_required("plans.get_dispatch_report")
    def dispatch_report(self, request, plans=None):
        """Cкачать диспетчерский отчет по периоду"""

        plans = self.filter_queryset(plans or self.get_queryset())
        plans = plans.order_by("assigned_date")

        if plans.count() == 0:
            return Response(
                {"error": "Нет планов для выбранных фильтров."},
                status=status.HTTP_404_NOT_FOUND,
            )

        start_date = request.GET.get("start_date", None)
        end_date = request.GET.get("end_date", None)

        if not start_date:
            start_date = plans.earliest("assigned_date").assigned_date
        else:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")

        if not end_date:
            end_date = plans.latest("assigned_date").assigned_date
        else:
            end_date = datetime.strptime(end_date, "%Y-%m-%d")

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

    @extend_schema(
        methods=["get"],
        description="Скачать план",
        filters=True,
        summary="Скачать план",
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
        plans = plans.order_by("assigned_date")

        if plans.count() == 0:
            return Response(
                {"error": "Нет планов для выбранных фильтров."},
                status=status.HTTP_404_NOT_FOUND,
            )

        start_date = request.GET.get("start_date", None)
        end_date = request.GET.get("end_date", None)

        if not start_date:
            start_date = plans.earliest("assigned_date").assigned_date
        else:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")

        if not end_date:
            end_date = plans.latest("assigned_date").assigned_date
        else:
            end_date = datetime.strptime(end_date, "%Y-%m-%d")

        buffer = generate_excelsheet_by_plan(plans, start_date, end_date)

        filename = f"ПЛАНЫ С {start_date.strftime('%d-%m-%Y')} ПО {end_date.strftime('%d-%m-%Y')}.xlsx"

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
        summary="Скачать отчет менеджера",
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
        manager: Manager = get_object_or_404(Manager, pk=manager_id)

        # Method export report is used here, because filters are applied here.
        plans = self.filter_queryset(plans or self.get_queryset())
        plans = plans.filter(managers__id=manager_id)
        plans = plans.order_by("assigned_date")

        if plans.count() == 0:
            return Response(
                {"error": "Нет планов для выбранных фильтров."},
                status=status.HTTP_404_NOT_FOUND,
            )

        start_date = request.GET.get("start_date", None)
        end_date = request.GET.get("end_date", None)

        if not start_date:
            start_date = plans.earliest("assigned_date").assigned_date
        else:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")

        if not end_date:
            end_date = plans.latest("assigned_date").assigned_date
        else:
            end_date = datetime.strptime(end_date, "%Y-%m-%d")

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
