from datetime import datetime, time
from math import atan2, cos, radians, sin, sqrt
from typing import Dict, List, Optional

from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.dateparse import parse_date, parse_datetime
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView

from api.v1.plans.serializers import PlanSerializer
from api.v1.users.serializers import GeoPointSerializer
from api.v1.utils.custom_permissions import IsAuthenticated
from managers.models import GeoPoint, Manager
from plans.models import Plan

GEOFENCE_RADIUS_METERS = 100


class CanViewDailyTracking(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm("managers.view_daily_tracking")


class DailyTrackingView(APIView):
    permission_classes = [IsAuthenticated, CanViewDailyTracking]

    def get(self, request):
        selected_date = parse_date(request.query_params.get("date", ""))
        manager_id = request.query_params.get("manager")

        if selected_date is None:
            return Response(
                {"error": "Передайте date в формате YYYY-MM-DD."}, status=400
            )
        if not manager_id:
            return Response({"error": "Передайте manager."}, status=400)

        manager_qs = Manager.objects.filter(is_hidden=False).filter(
            Q(is_manager=True) | Q(is_driver=True)
        )
        manager = get_object_or_404(manager_qs, pk=manager_id)

        plans = list(
            Plan.objects.filter(assigned_date=selected_date, managers=manager)
            .select_related("client", "client__address")
            .prefetch_related("work_items", "managers")
            .order_by("created_at", "id")
        )

        all_geopoints_qs = GeoPoint.objects.filter(
            manager=manager,
            created_at__gte=datetime.combine(selected_date, time.min),
            created_at__lte=datetime.combine(selected_date, time.max),
        ).order_by("created_at", "id")
        all_geopoints = list(all_geopoints_qs)
        delta_geopoints = self._filter_delta(all_geopoints, request.query_params)

        current_geopoint = all_geopoints[-1] if all_geopoints else None
        cursor = self._cursor_for(current_geopoint)
        response = {
            "date": selected_date.isoformat(),
            "manager": self._serialize_manager(manager),
            "plans": PlanSerializer(plans, many=True).data,
            "geopoints": GeoPointSerializer(delta_geopoints, many=True).data,
            "current_geopoint": GeoPointSerializer(current_geopoint).data
            if current_geopoint
            else None,
            "cursor": cursor,
            "timeline": build_timeline(plans, all_geopoints),
        }

        return Response(response)

    def _has_cursor(self, query_params):
        return bool(query_params.get("since_created_at") or query_params.get("since"))

    def _filter_delta(self, geopoints: List[GeoPoint], query_params) -> List[GeoPoint]:
        since_raw = query_params.get("since_created_at") or query_params.get("since")
        if not since_raw:
            return geopoints

        since_created_at = parse_datetime(since_raw)
        if since_created_at is None:
            return []
        if timezone.is_aware(since_created_at):
            since_created_at = timezone.make_naive(since_created_at)

        since_id = query_params.get("since_id")
        since_id_int = int(since_id) if since_id and since_id.isdigit() else None

        delta = []
        for geopoint in geopoints:
            if geopoint.created_at > since_created_at:
                delta.append(geopoint)
            elif (
                since_id_int is not None
                and geopoint.created_at == since_created_at
                and geopoint.id > since_id_int
            ):
                delta.append(geopoint)
        return delta

    def _cursor_for(self, geopoint: Optional[GeoPoint]):
        if geopoint is None:
            return None
        return {
            "created_at": geopoint.created_at.isoformat(),
            "id": str(geopoint.id),
        }

    def _serialize_manager(self, manager: Manager):
        return {
            "id": str(manager.id),
            "name": manager.name,
            "is_manager": manager.is_manager,
            "is_driver": manager.is_driver,
            "depot_lat": float(manager.depot_lat) if manager.depot_lat else None,
            "depot_lon": float(manager.depot_lon) if manager.depot_lon else None,
        }


def build_timeline(plans: List[Plan], geopoints: List[GeoPoint]):
    if not plans or not geopoints:
        return []

    trackable_plans = [plan for plan in plans if has_plan_location(plan)]
    if not trackable_plans:
        return []

    assignments = [
        nearest_inside_plan(geopoint, trackable_plans) for geopoint in geopoints
    ]
    visits = build_visit_intervals(assignments, geopoints)
    rows = []

    for index, visit in enumerate(visits):
        if index == 0:
            rows.append(build_first_travel_row(visit, geopoints))
        else:
            rows.append(build_travel_row(visits[index - 1], visit, geopoints))
        rows.append(build_inside_row(visit, geopoints))

    return rows


def has_plan_location(plan: Plan) -> bool:
    return bool(
        plan.client
        and plan.client.address
        and plan.client.address.lat is not None
        and plan.client.address.lon is not None
    )


def nearest_inside_plan(geopoint: GeoPoint, plans: List[Plan]) -> Optional[Plan]:
    nearest_plan = None
    nearest_distance = None

    for plan in plans:
        distance = haversine_meters(
            float(geopoint.latitude),
            float(geopoint.longitude),
            float(plan.client.address.lat),
            float(plan.client.address.lon),
        )
        radius = max(GEOFENCE_RADIUS_METERS, geopoint.accuracy or 0)
        if distance <= radius and (
            nearest_distance is None or distance < nearest_distance
        ):
            nearest_distance = distance
            nearest_plan = plan

    return nearest_plan


def build_visit_intervals(assignments: List[Optional[Plan]], geopoints: List[GeoPoint]):
    visits = []
    active_plan = None
    start_index = None

    for index, plan in enumerate(assignments):
        if active_plan and (plan is None or plan.id != active_plan.id):
            visits.append(
                {
                    "plan": active_plan,
                    "start_index": start_index,
                    "end_index": index - 1,
                }
            )
            active_plan = None
            start_index = None

        if plan and active_plan is None:
            active_plan = plan
            start_index = index

    if active_plan:
        visits.append(
            {
                "plan": active_plan,
                "start_index": start_index,
                "end_index": len(geopoints) - 1,
            }
        )

    return visits


def build_first_travel_row(visit: Dict, geopoints: List[GeoPoint]):
    start_index = 0
    end_index = visit["start_index"]
    return build_row(
        row_id=f"travel-depot-{visit['plan'].id}-{start_index}-{end_index}",
        row_type="travel",
        type_label="В пути",
        route=f"Дом → {visit['plan'].client.name}",
        start_geopoint=geopoints[start_index],
        end_geopoint=geopoints[end_index],
        geopoints=geopoints[start_index : end_index + 1],
        to_plan_id=str(visit["plan"].id),
    )


def build_travel_row(previous_visit: Dict, next_visit: Dict, geopoints: List[GeoPoint]):
    start_index = previous_visit["end_index"]
    end_index = next_visit["start_index"]
    return build_row(
        row_id=(
            f"travel-{previous_visit['plan'].id}-{next_visit['plan'].id}-"
            f"{start_index}-{end_index}"
        ),
        row_type="travel",
        type_label="В пути",
        route=(
            f"{previous_visit['plan'].client.name} → "
            f"{next_visit['plan'].client.name}"
        ),
        start_geopoint=geopoints[start_index],
        end_geopoint=geopoints[end_index],
        geopoints=geopoints[start_index : end_index + 1],
        from_plan_id=str(previous_visit["plan"].id),
        to_plan_id=str(next_visit["plan"].id),
    )


def build_inside_row(visit: Dict, geopoints: List[GeoPoint]):
    start_index = visit["start_index"]
    end_index = visit["end_index"]
    return build_row(
        row_id=f"inside-{visit['plan'].id}-{start_index}-{end_index}",
        row_type="inside_plan",
        type_label="На точке",
        route=visit["plan"].client.name,
        start_geopoint=geopoints[start_index],
        end_geopoint=geopoints[end_index],
        geopoints=geopoints[start_index : end_index + 1],
        plan_id=str(visit["plan"].id),
    )


def build_row(
    row_id: str,
    row_type: str,
    type_label: str,
    route: str,
    start_geopoint: GeoPoint,
    end_geopoint: GeoPoint,
    geopoints: List[GeoPoint],
    plan_id: Optional[str] = None,
    from_plan_id: Optional[str] = None,
    to_plan_id: Optional[str] = None,
):
    return {
        "id": row_id,
        "type": row_type,
        "type_label": type_label,
        "route": route,
        "start_at": start_geopoint.created_at.isoformat(),
        "end_at": end_geopoint.created_at.isoformat(),
        "duration_seconds": int(
            max(
                (end_geopoint.created_at - start_geopoint.created_at).total_seconds(),
                0,
            )
        ),
        "plan_id": plan_id,
        "from_plan_id": from_plan_id,
        "to_plan_id": to_plan_id,
        "geopoint_ids": [str(geopoint.id) for geopoint in geopoints],
    }


def haversine_meters(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    earth_radius_meters = 6371000
    phi1 = radians(lat1)
    phi2 = radians(lat2)
    delta_phi = radians(lat2 - lat1)
    delta_lambda = radians(lon2 - lon1)

    a = (
        sin(delta_phi / 2) ** 2
        + cos(phi1) * cos(phi2) * sin(delta_lambda / 2) ** 2
    )
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return earth_radius_meters * c
