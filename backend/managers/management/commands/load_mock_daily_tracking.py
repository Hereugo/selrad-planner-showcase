from datetime import datetime, time, timedelta
from math import atan2, cos, radians, sin, sqrt
from typing import Iterable, Optional, Tuple

from django.contrib.gis.geos import Point
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.db.models import Q
from django.utils.dateparse import parse_date, parse_time

from managers.models import GeoPoint, Manager
from plans.models import Plan

Coordinate = Tuple[float, float]


class Command(BaseCommand):
    help = "Load mock geopoints for testing the Daily Tracking page."

    def add_arguments(self, parser):
        parser.add_argument(
            "--manager-id",
            help="Driver/manager id. If omitted, the command picks a recent driver with plans.",
        )
        parser.add_argument(
            "--date",
            help="Plan/geopoint date in YYYY-MM-DD. If omitted, the command picks a recent date.",
        )
        parser.add_argument(
            "--start-time",
            default="09:00",
            help="Mock route start time in HH:MM. Default: 09:00.",
        )
        parser.add_argument(
            "--points-per-leg",
            type=int,
            default=8,
            help="Moving geopoints generated between stops. Default: 8.",
        )
        parser.add_argument(
            "--stop-points",
            type=int,
            default=4,
            help="Inside-geofence geopoints generated at each plan. Default: 4.",
        )
        parser.add_argument(
            "--max-plans",
            type=int,
            default=4,
            help="Maximum assigned plans to include in the mock route. Default: 4.",
        )
        parser.add_argument(
            "--replace",
            action="store_true",
            help="Delete existing geopoints for the selected manager/date before inserting mock data.",
        )
        parser.add_argument(
            "--list-candidates",
            action="store_true",
            help="Print recent driver/date candidates and exit.",
        )

    def handle(self, *args, **options):
        if options["list_candidates"]:
            self.print_candidates()
            return

        selected_date = parse_date(options.get("date") or "")
        start_time = parse_time(options["start_time"])
        if options.get("date") and selected_date is None:
            raise CommandError("--date must be in YYYY-MM-DD format.")
        if start_time is None:
            raise CommandError("--start-time must be in HH:MM format.")
        if options["points_per_leg"] < 1:
            raise CommandError("--points-per-leg must be at least 1.")
        if options["stop_points"] < 1:
            raise CommandError("--stop-points must be at least 1.")
        if options["max_plans"] < 1:
            raise CommandError("--max-plans must be at least 1.")

        manager = self.get_manager(options.get("manager_id"))
        if selected_date is None:
            selected_date = self.pick_date(manager)
        if selected_date is None:
            raise CommandError("No candidate date found for mock daily tracking data.")

        plans = list(
            Plan.objects.filter(
                assigned_date=selected_date,
                managers=manager,
                client__address__lat__isnull=False,
                client__address__lon__isnull=False,
            )
            .select_related("client", "client__address")
            .order_by("created_at", "id")[: options["max_plans"]]
        )
        if not plans:
            raise CommandError(
                f"No plans with coordinates found for {manager} on {selected_date}."
            )

        geopoints = build_mock_geopoints(
            manager=manager,
            plans=plans,
            route_date=selected_date,
            start_time=start_time,
            points_per_leg=options["points_per_leg"],
            stop_points=options["stop_points"],
        )

        with transaction.atomic():
            if options["replace"]:
                deleted_count = GeoPoint.objects.filter(
                    manager=manager,
                    created_at__gte=datetime.combine(selected_date, time.min),
                    created_at__lte=datetime.combine(selected_date, time.max),
                ).delete()[0]
                self.stdout.write(f"Deleted existing geopoints: {deleted_count}")

            mock_created_at_values = [geopoint.created_at for geopoint in geopoints]
            created = GeoPoint.objects.bulk_create(geopoints)
            # auto_now_add sets created_at to now; update to the mock route times.
            for created_point, mock_created_at in zip(created, mock_created_at_values):
                created_point.created_at = mock_created_at
            GeoPoint.objects.bulk_update(created, ["created_at"])

        self.stdout.write(self.style.SUCCESS(f"Created geopoints: {len(created)}"))
        self.stdout.write(f"Manager: {manager.id} | {manager.name}")
        self.stdout.write(f"Date: {selected_date.isoformat()}")
        self.stdout.write("Plans:")
        for plan in plans:
            self.stdout.write(f"- {plan.id} | {plan.client.name}")
        self.stdout.write(
            self.style.NOTICE(
                "Open /daily_tracking and select the manager/date above to inspect it."
            )
        )

    def get_manager(self, manager_id: Optional[str]) -> Manager:
        qs = Manager.objects.filter(is_hidden=False).filter(
            Q(is_driver=True) | Q(is_manager=True)
        )
        if manager_id:
            try:
                return qs.get(id=manager_id)
            except Manager.DoesNotExist as exc:
                raise CommandError(f"No visible driver/manager found: {manager_id}") from exc

        candidate = self.candidates().first()
        if candidate is None:
            raise CommandError("No driver/manager with assigned plans was found.")
        return candidate["manager"]

    def pick_date(self, manager: Manager):
        plan = (
            Plan.objects.filter(
                managers=manager,
                client__address__lat__isnull=False,
                client__address__lon__isnull=False,
            )
            .order_by("-assigned_date", "created_at")
            .first()
        )
        return plan.assigned_date if plan else None

    def candidates(self):
        seen = set()
        candidates = []
        plans = (
            Plan.objects.filter(
                managers__is_hidden=False,
                client__address__lat__isnull=False,
                client__address__lon__isnull=False,
            )
            .filter(Q(managers__is_driver=True) | Q(managers__is_manager=True))
            .select_related("client", "client__address")
            .prefetch_related("managers")
            .order_by("-assigned_date", "created_at")[:200]
        )

        for plan in plans:
            manager = next(
                (
                    person
                    for person in plan.managers.all()
                    if not person.is_hidden and (person.is_driver or person.is_manager)
                ),
                None,
            )
            if manager is None:
                continue

            key = (manager.id, plan.assigned_date)
            if key in seen:
                continue
            seen.add(key)
            plan_count = Plan.objects.filter(
                assigned_date=plan.assigned_date,
                managers=manager,
                client__address__lat__isnull=False,
                client__address__lon__isnull=False,
            ).count()
            candidates.append(
                {
                    "manager": manager,
                    "date": plan.assigned_date,
                    "plan_count": plan_count,
                }
            )

        return CandidateList(candidates)

    def print_candidates(self):
        candidates = self.candidates().items[:20]
        if not candidates:
            self.stdout.write("No candidates found.")
            return

        for candidate in candidates:
            manager = candidate["manager"]
            self.stdout.write(
                f"manager={manager.id} date={candidate['date']} "
                f"plans={candidate['plan_count']} name={manager.name}"
            )


class CandidateList:
    def __init__(self, items):
        self.items = items

    def first(self):
        return self.items[0] if self.items else None


def build_mock_geopoints(
    manager: Manager,
    plans: Iterable[Plan],
    route_date,
    start_time,
    points_per_leg: int,
    stop_points: int,
):
    current_at = datetime.combine(route_date, start_time)
    plan_coordinates = [plan_coordinate(plan) for plan in plans]
    current_coordinate = starting_coordinate(manager, plan_coordinates[0])
    geopoints = []

    for destination in plan_coordinates:
        leg = interpolate(current_coordinate, destination, points_per_leg)
        previous_coordinate = current_coordinate
        for coordinate in leg:
            current_at += timedelta(minutes=3)
            geopoints.append(
                geopoint(
                    manager=manager,
                    coordinate=coordinate,
                    created_at=current_at,
                    speed=speed_between(previous_coordinate, coordinate, 180),
                    heading=bearing(previous_coordinate, coordinate),
                    accuracy=15,
                )
            )
            previous_coordinate = coordinate

        for index in range(stop_points):
            current_at += timedelta(minutes=2)
            stop_coordinate = offset_coordinate(destination, index)
            geopoints.append(
                geopoint(
                    manager=manager,
                    coordinate=stop_coordinate,
                    created_at=current_at,
                    speed=0,
                    heading=bearing(previous_coordinate, stop_coordinate),
                    accuracy=12,
                )
            )
            previous_coordinate = stop_coordinate

        current_coordinate = destination
        current_at += timedelta(minutes=4)

    return geopoints


def plan_coordinate(plan: Plan) -> Coordinate:
    return (float(plan.client.address.lat), float(plan.client.address.lon))


def starting_coordinate(manager: Manager, first_plan: Coordinate) -> Coordinate:
    if manager.depot_lat is not None and manager.depot_lon is not None:
        return (float(manager.depot_lat), float(manager.depot_lon))
    return (first_plan[0] - 0.025, first_plan[1] - 0.025)


def interpolate(start: Coordinate, end: Coordinate, count: int):
    return [
        (
            start[0] + (end[0] - start[0]) * (index / count),
            start[1] + (end[1] - start[1]) * (index / count),
        )
        for index in range(1, count + 1)
    ]


def offset_coordinate(coordinate: Coordinate, index: int) -> Coordinate:
    offsets_meters = [(0, 0), (12, 8), (-10, 6), (7, -11), (-8, -9)]
    north_meters, east_meters = offsets_meters[index % len(offsets_meters)]
    lat = coordinate[0] + north_meters / 111_320
    lon = coordinate[1] + east_meters / (111_320 * cos(radians(coordinate[0])))
    return (lat, lon)


def geopoint(
    manager: Manager,
    coordinate: Coordinate,
    created_at: datetime,
    speed: float,
    heading: float,
    accuracy: float,
):
    return GeoPoint(
        manager=manager,
        latitude=round(coordinate[0], 6),
        longitude=round(coordinate[1], 6),
        point=Point(coordinate[1], coordinate[0]),
        accuracy=accuracy,
        speed=round(speed, 2),
        heading=round(heading, 2),
        created_at=created_at,
    )


def speed_between(start: Coordinate, end: Coordinate, seconds: int) -> float:
    return haversine_meters(start, end) / seconds


def bearing(start: Coordinate, end: Coordinate) -> float:
    lat1 = radians(start[0])
    lat2 = radians(end[0])
    delta_lon = radians(end[1] - start[1])
    y = sin(delta_lon) * cos(lat2)
    x = cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(delta_lon)
    return (atan2(y, x) * 180 / 3.141592653589793 + 360) % 360


def haversine_meters(start: Coordinate, end: Coordinate) -> float:
    earth_radius_meters = 6_371_000
    lat1 = radians(start[0])
    lat2 = radians(end[0])
    delta_lat = radians(end[0] - start[0])
    delta_lon = radians(end[1] - start[1])
    a = sin(delta_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(delta_lon / 2) ** 2
    return earth_radius_meters * 2 * atan2(sqrt(a), sqrt(1 - a))
