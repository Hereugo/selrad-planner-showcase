import datetime

from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.v1.utils.custom_permissions import IsAuthenticated
from clients.models import Client
from managers.models import Manager
from optimization.metrics import two_opt_tour, cheapest_insertion_cost
from plans.models import Plan


class ManagerScoresView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        parameters=[
            OpenApiParameter(name="date", type=datetime.date, required=True),
            OpenApiParameter(name="client_id", type=str, required=True),
            OpenApiParameter(name="plan_id", type=int, required=False),
        ]
    )
    def get(self, request: Request) -> Response:
        date_str = request.query_params.get("date")
        client_id = request.query_params.get("client_id")
        plan_id_str = request.query_params.get("plan_id")

        if not date_str or not client_id:
            return Response(
                {"error": "date and client_id are required"}, status=400
            )

        try:
            target_date = datetime.date.fromisoformat(date_str)
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD"}, status=400)

        try:
            new_client = Client.objects.select_related("address").get(pk=client_id)
        except Client.DoesNotExist:
            return Response({"error": "Client not found"}, status=404)

        skip_route = new_client.name == "ВЫХОДНОЙ"

        excluded_plan_id = None
        if plan_id_str is not None:
            try:
                excluded_plan = Plan.objects.get(pk=int(plan_id_str))
                excluded_plan_id = excluded_plan.pk
            except (ValueError, TypeError, Plan.DoesNotExist):
                return Response({"error": "Plan not found"}, status=404)

        addr = new_client.address
        if addr is not None and (float(addr.lat) != 0 or float(addr.lon) != 0):
            new_stop: tuple[float, float] | None = (float(addr.lat), float(addr.lon))
        else:
            new_stop = None

        managers = Manager.objects.filter(
            is_manager=True,
            is_warehouser=False,
            depot_lat__isnull=False,
            depot_lon__isnull=False,
        )

        results = []
        for manager in managers:
            depot = (float(manager.depot_lat), float(manager.depot_lon))

            # Check if the manager has a ВЫХОДНОЙ (day-off) plan on this date.
            # If they do, they are unavailable — skip them from scoring.
            day_off_qs = Plan.objects.filter(
                assigned_date=target_date,
                managers=manager,
                client__name="ВЫХОДНОЙ",
            )
            if excluded_plan_id is not None:
                day_off_qs = day_off_qs.exclude(pk=excluded_plan_id)
            if day_off_qs.exists():
                results.append({
                    "manager_id": str(manager.id),
                    "workload": 0,
                    "route_km_delta": 0.0,
                    "is_day_off": True,
                })
                continue

            existing_plans = Plan.objects.filter(
                assigned_date=target_date,
                managers=manager,
            ).exclude(client__name="ВЫХОДНОЙ")
            if excluded_plan_id is not None:
                existing_plans = existing_plans.exclude(pk=excluded_plan_id)
            existing_plans = existing_plans.select_related("client__address")

            stops = []
            for plan in existing_plans:
                if plan.client and plan.client.address:
                    a = plan.client.address
                    lat, lon = float(a.lat), float(a.lon)
                    if lat != 0 or lon != 0:
                        stops.append((lat, lon))

            workload = existing_plans.count()

            if skip_route:
                results.append({
                    "manager_id": str(manager.id),
                    "workload": workload,
                })
            else:
                if new_stop is None:
                    delta = 0.0
                else:
                    tour = two_opt_tour(stops, depot)
                    delta = round(cheapest_insertion_cost(tour, depot, new_stop), 2)

                results.append({
                    "manager_id": str(manager.id),
                    "workload": workload,
                    "route_km_delta": delta,
                })

        return Response(results)
