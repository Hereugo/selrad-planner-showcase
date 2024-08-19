import logging

from datetime import datetime
from django.http import HttpResponse
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.permissions import BasePermission
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet, GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from drf_spectacular.utils import (
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
    PlanSerializer,
    PlanUpdateSerializer,
    WorkItemSerializer,
)
from .work_items_serializers import TaskSerializer, TaskUpdatePolymorphicSerializer

from .custom_permissions import CanChangeFuturePlans, CanDeleteFuturePlans
from .custom_filters import PlanFilter, TaskFilter
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
        "managers__first_name",
        "work_items__name",
    )

    def get_permissions(self):
        permission_classes: list[type[BasePermission]] = [IsAuthenticated]
        if self.action in ("update", "partial_update"):
            permission_classes.append(CanChangeFuturePlans)
        elif self.action == "destroy":
            permission_classes.append(CanDeleteFuturePlans)

        permission_classes.append(HasCRUDPermission)

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return PlanUpdateSerializer

        return super().get_serializer_class()

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

        plans: QuerySet[Plan] = self.filter_queryset(self.get_queryset())
        manager: Manager = get_object_or_404(Manager, id=manager_id)

        if not start_date:
            start_date = plans.latest("assigned_date").assigned_date
        else:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")

        if not end_date:
            end_date = plans.earliest("assigned_date").assigned_date
        else:
            end_date = datetime.strptime(end_date, "%Y-%m-%d")

        buffer = generate_dispatch_list(plans, manager, comment, start_date, end_date)
        filename: str = (
            f"ДИСПЕТЧЕРСКИЙ ЛИСТ С {end_date.strftime('%d-%m-%Y')} ПО {start_date.strftime('%d-%m-%Y')}.xlsx"
        )

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

        if plans.count() == 0:
            return Response(
                {"error": "Нет планов для выбранных фильтров."},
                status=status.HTTP_404_NOT_FOUND,
            )

        start_date = request.GET.get("start_date", None)
        end_date = request.GET.get("end_date", None)

        if not start_date:
            start_date = plans.latest("assigned_date").assigned_date
        else:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")

        if not end_date:
            end_date = plans.earliest("assigned_date").assigned_date
        else:
            end_date = datetime.strptime(end_date, "%Y-%m-%d")

        buffer = generate_excelsheet_by_plan(plans, start_date, end_date)

        filename = f"ПЛАНЫ С {end_date.strftime('%d-%m-%Y')} ПО {start_date.strftime('%d-%m-%Y')}.xlsx"

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
        manager = get_object_or_404(Manager, pk=manager_id)

        # Method export report is used here, because filters are applied here.
        plans = self.filter_queryset(plans or self.get_queryset())
        plans = plans.filter(managers__id=manager_id)

        if plans.count() == 0:
            return Response(
                {"error": "Нет планов для выбранных фильтров."},
                status=status.HTTP_404_NOT_FOUND,
            )

        start_date = request.GET.get("start_date", None)
        end_date = request.GET.get("end_date", None)

        if not start_date:
            start_date = plans.latest("assigned_date").assigned_date
        else:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")

        if not end_date:
            end_date = plans.earliest("assigned_date").assigned_date
        else:
            end_date = datetime.strptime(end_date, "%Y-%m-%d")

        buffer = generate_excelsheet_by_manager(plans, manager, end_date, start_date)

        filename = f"ОТЧЕТ {manager} С {end_date.strftime('%d-%m-%Y')} ПО {start_date.strftime('%d-%m-%Y')}.xlsx"

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

    queryset = PlanWorkItem.objects.filter(work_item__show_on_main_page=True)
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
