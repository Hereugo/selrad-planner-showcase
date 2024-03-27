import logging

from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action 
from rest_framework.response import Response 
from rest_framework.schemas.openapi import AutoSchema
from drf_spectacular.utils import extend_schema, OpenApiParameter
from django.http import HttpResponse

from plans.models import Plan, Worklist

from api.utils.custom_permissions import IsAuthenticated 
from api.utils.custom_paginations import PageLimitPagination
from .serializers import PlanSerializer, PlanUpdateSerializer, WorklistSerializer 
from .custom_filters import PlanFilter
from .generate_excelsheet import generate_excelsheet_by_plan, generate_excelsheet_by_manager


logger = logging.getLogger(__name__)


class PlanViewSet(ModelViewSet):
    """API для работы с планами."""

    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    pagination_class = PageLimitPagination
    filter_backends = (DjangoFilterBackend,
                       filters.SearchFilter,
                       filters.OrderingFilter)
    filterset_class = PlanFilter
    search_fields = ('client__name', 'managers__first_name', 'worklist__name', )

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return PlanUpdateSerializer

        return super().get_serializer_class()

    @extend_schema(
        methods=['get'],
        filters=True
    )
    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated],
        url_path='export',
    )
    def export(self, request):
        """Скачать план."""

        plans = self.filter_queryset(self.get_queryset())
        
        buffer = generate_excelsheet_by_plan(plans)
      
        # TODO: Add from what daterange 
        filename = 'планы.xlsx'

        response = HttpResponse(buffer.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response

    @extend_schema(
        methods=['get'],
        parameters=[
            OpenApiParameter(
                'managers',
                str,
                OpenApiParameter.QUERY,
                description='Список ids менеджеров'
            )
        ],
    )
    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated],
        url_path='export_by_managers',
    )
    def export_by_managers(self, request):
        """Скачать план."""
        # get from request manager ids
        manager_ids = request.GET.get('managers', '').split(',')

        plans = self.filter_queryset(self.get_queryset())
        # managers = Manager.objects.get(pk__in=manager_ids) 

        buffer = generate_excelsheet_by_manager(plans, manager_ids)
      
        # TODO: Add from what daterange 
        filename = 'отчет.xlsx'

        response = HttpResponse(buffer.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response


class WorklistViewSet(ModelViewSet):
    """API для работы с рабочими списками."""

    queryset = Worklist.objects.all()
    serializer_class = WorklistSerializer
    pagiation_class = None
