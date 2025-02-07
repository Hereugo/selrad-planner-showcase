import logging
from datetime import datetime, timedelta

from api.plans.serializers import NearbyClientSerializer
from api.utils.custom_permissions import IsAuthenticated
from clients.models import Client
from django.contrib.gis.measure import Distance
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from .serializers import ClientSerializer

logger = logging.getLogger()


class ClientViewSet(ReadOnlyModelViewSet):
    """API для работы с клиентами."""

    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    pagination_class = None

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
