import logging

from api.exports.custom_schemas import *
from api.utils.custom_paginations import PageLimitPagination
from api.utils.custom_permissions import HasCRUDPermission, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from plans.models import PaymentRegistry, Plan, PlanWorkItem, WorkItem
from rest_framework import filters
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet, ReadOnlyModelViewSet

from .custom_filters import PaymentRegistryFilter, PlanFilter, TaskFilter
from .custom_permissions import CanDeleteFuturePlans
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


# NOTE (Amir Nurmukhambetov 04/01/2025):
#
# This class is made to have file exports be in seperate files.
# Before this refactor PlanViewSet contained all actions for exports which made
# it hard to add more new file exports.
#
# Side note, we can't use PlanViewSet directly because of ModelViewSet.
# Other classes would inherit it from PlanViewSet and make swagger look ugly and
# bloated with uncessary endpoints.
class GenericPlanViewSet:
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


class PlanViewSet(GenericPlanViewSet, ModelViewSet):
    """API для работы с планами."""

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
