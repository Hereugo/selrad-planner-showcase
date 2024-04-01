import logging

from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance

from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action 
from drf_spectacular.utils import extend_schema, OpenApiParameter

from api.utils.custom_permissions import IsAuthenticated 

from clients.models import Client
from .serializers import ClientSerializer 


logger = logging.getLogger(__name__)


class ClientViewSet(ModelViewSet):
    """API для работы с клиентами."""

    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    pagination_class = None

    @extend_schema(
        methods=['get'],
        parameters=[
            OpenApiParameter(
                'radius',
                float,
                OpenApiParameter.QUERY,
                description='Радиус поиска в км',
                default=0.5
            ),
            OpenApiParameter(
                'time_threshold',
                int,
                OpenApiParameter.QUERY,
                description='Порог времени в днях',
                default=30
            )
        ],
        responses={
            200: ClientSerializer(many=True)
        }
    )
    @action(
        detail=True,
        methods=['get'],
        permission_classes=[IsAuthenticated],
        url_path='find_nearby',
    )
    def find_nearby(self, request, pk=None):
        """Найти ближайшие планы."""

        client = get_object_or_404(Client, pk=pk)
        radius = float(request.GET.get('radius', 0.5))
        time_threshold = int(request.GET.get('time_threshold', 30))

        nearby_clients = Client.objects.filter(
            address__point__distance_lte=(
                client.address.point,
                Distance(km=radius)
            )
        ).exclude(pk=pk)

        nearby_clients = nearby_clients.filter(
            plans__assigned_date__gte=client.plans.last().assigned_date + timezone.timedelta(days=time_threshold)
        )

        serializer = ClientSerializer(nearby_clients, many=True)
        return Response(serializer.data)
