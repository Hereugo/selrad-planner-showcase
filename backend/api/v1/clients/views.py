import logging
from datetime import datetime, timedelta

from django.contrib.gis.measure import Distance
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from api.v1.clients.serializers import (
    ClientCreateSerializer,
    ClientSerializer,
    MetaClientSerializer,
)
from api.v1.plans.serializers import NearbyClientSerializer
from api.v1.utils.custom_permissions import IsAuthenticated
from clients.models import Client, MetaClient

logger = logging.getLogger(__name__)


class CanAddClient(BasePermission):
    """Allow creating shops only with Django add permission."""

    def has_permission(self, request, view):
        return request.user.has_perm("clients.add_client")


class ClientViewSet(CreateModelMixin, ReadOnlyModelViewSet):
    """API для работы с клиентами."""

    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    pagination_class = None

    def get_permissions(self):
        if self.action == "create":
            return [IsAuthenticated(), CanAddClient()]

        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == "create":
            return ClientCreateSerializer

        return super().get_serializer_class()

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
                "min_days_since_plan",
                int,
                OpenApiParameter.QUERY,
                description="Порог времени в днях",
                default=10,
            ),
            OpenApiParameter(
                "from_date",
                str,
                OpenApiParameter.QUERY,
                description="Дата начала периода",
                default=datetime.now().strftime("%Y-%m-%d"),
            ),
        ],
        summary="Найти ближайших клиентов",
        responses={200: NearbyClientSerializer(many=True)},
    )
    @action(
        detail=True,
        methods=["get"],
        permission_classes=[IsAuthenticated],
        url_path="find_nearby",
    )
    def find_nearby(self, request, pk=None):
        """Найти ближайших клиентов по текущему клиенту."""
        client = get_object_or_404(Client, pk=pk)
        radius = float(request.GET.get("radius", 0.5))
        min_days_since_plan = int(request.GET.get("min_days_since_plan", 10))
        from_date = datetime.strptime(
            request.GET.get("from_date", datetime.now().strftime("%Y-%m-%d")),
            "%Y-%m-%d",
        )
        # get all clients that are in the radius of a circle [plan.client.address.point, radius]
        nearby_clients = Client.objects.filter(
            address__point__distance_lte=(
                client.address.point,
                Distance(km=radius),
            )
        ).exclude(pk=pk)

        exclude_clients = []
        for nc in nearby_clients:
            last_plan = nc.plans.order_by("-assigned_date").first()
            offset = timedelta(days=min_days_since_plan)
            if last_plan and last_plan.assigned_date > (from_date - offset).date():
                exclude_clients.append(nc.pk)

        a = nearby_clients.exclude(pk__in=exclude_clients)

        # get all clients that have no plans
        b = nearby_clients.filter(plans__isnull=True)
        nearby_clients = a | b

        # remove all duplicates
        nearby_clients = nearby_clients.distinct()

        nearby_clients = nearby_clients.filter(is_hidden_on_map=False)

        serializer = NearbyClientSerializer(nearby_clients, many=True)

        return Response(serializer.data)


class MetaClientViewSet(ReadOnlyModelViewSet):
    """API для работы с клиентами компаний."""

    queryset = MetaClient.objects.all()
    serializer_class = MetaClientSerializer
    pagination_class = None
