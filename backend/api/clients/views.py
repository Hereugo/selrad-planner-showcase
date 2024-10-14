import logging
from datetime import datetime


from django.shortcuts import get_object_or_404
from datetime import timedelta
from django.http import HttpResponse
from django.contrib.gis.measure import Distance
from rest_framework.decorators import action
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter

from api.utils.custom_permissions import IsAuthenticated
from api.plans.serializers import NearbyClientSerializer
from api.utils.custom_permissions import (
    IsAuthenticated,
    permission_required,
)

from clients.models import Client
from .serializers import ClientSerializer
from .generate_compare_years import generate_compare_years

logger = logging.getLogger(__name__)


class ClientViewSet(ReadOnlyModelViewSet):
    """API для работы с клиентами."""

    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    pagination_class = None

    @extend_schema(
        methods=["get"],
        description="Скачать сравнить по периодам",
        filters=True,
        summary="Скачать сравнить по периодам",
        parameters=[
            OpenApiParameter("start_date", str),
            OpenApiParameter("end_date", str),
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
            "start": datetime.strptime(start_date, "%Y-%m-%d"),
            "end": datetime.strptime(end_date, "%Y-%m-%d"),
        }
        period_1 = period_2.copy()
        period_1["start"] = period_1["start"].replace(
            year=period_1["start"].year - to_year_diff
        )
        period_1["end"] = period_1["end"].replace(
            year=period_1["end"].year - to_year_diff
        )

        buffer = generate_compare_years(period_1, period_2)

        filename = f"СРАВНИТЬ {period_1['start'].strftime('%d-%m-%Y')} ПО {period_1['end'].strftime('%d-%m-%Y')} ПРОТИВ {period_2['start'].strftime('%d-%m-%Y')} ПО {period_2['end'].strftime('%d-%m-%Y')} ГОДА.xlsx"

        response = HttpResponse(
            buffer.getvalue(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Access-Control-Expose-Headers"] = "Content-Disposition"
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
