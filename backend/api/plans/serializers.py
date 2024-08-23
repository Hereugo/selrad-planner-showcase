import logging
from typing import Any, Optional, List

from rest_framework import serializers

from api.clients.serializers import ClientSerializer
from api.users.serializers import ManagerSerializer

from clients.models import Client
from managers.models import Manager
from plans.models import Plan, WorkItem, PlanWorkItem, PlanManager


logger = logging.getLogger(__name__)


class WorkItemSerializer(serializers.ModelSerializer):
    """Serializer for WorkItem model"""

    id = serializers.StringRelatedField()

    class Meta:
        model = WorkItem
        fields = (
            "id",
            "name",
        )


class PlanSerializer(serializers.ModelSerializer):
    """Serializer for Plan model"""

    id = serializers.StringRelatedField()
    work_items = WorkItemSerializer(many=True)
    client = ClientSerializer()
    managers = ManagerSerializer(many=True)

    class Meta:
        model = Plan
        fields = (
            "id",
            "assigned_date",
            "work_items",
            "client",
            "shipment_cost_formula",
            "shipment_cost",
            "comment",
            "managers",
            "box_count",
            "created_at",
            "updated_at",
        )


class PlanUpdateSerializer(serializers.ModelSerializer):
    """Serializer for Plan model"""

    id = serializers.StringRelatedField()
    work_items = serializers.PrimaryKeyRelatedField(
        queryset=WorkItem.objects.all(),
        many=True,
        required=False,
    )
    managers = serializers.PrimaryKeyRelatedField(
        queryset=Manager.objects.all(),
        many=True,
        required=False,
    )
    client = serializers.PrimaryKeyRelatedField(
        queryset=Client.objects.all(),
        required=False,
    )

    class Meta:
        model = Plan
        fields = (
            "id",
            "assigned_date",
            "work_items",
            "client",
            "shipment_cost_formula",
            "shipment_cost",
            "comment",
            "managers",
            "box_count",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")

    def validate(self, attrs):
        # If work_items contains a "shipment" type, then only one manager should be assgined as driver
        work_items: List[WorkItem] = attrs.get("work_items", [])
        managers: List[Manager] = attrs.get("managers", [])

        if any(
            work_item.content_type.model_class().__name__.lower() == "shipment"
            for work_item in work_items
            if work_item.content_type
        ):
            drivers: List[Manager] = list(filter(lambda x: x.is_driver, managers))

            if len(drivers) > 1:
                raise serializers.ValidationError(
                    f"При наличии отгрузки, должен быть назначен только один водитель. Водители: {', '.join([d.name for d in drivers])}"
                )
            elif len(drivers) == 0:
                raise serializers.ValidationError(
                    "При наличии отгрузки, должен быть назначен хотя бы один водитель"
                )

        return super().validate(attrs)

    def create_work_items(self, plan: Plan, work_items: List[WorkItem]):
        plan_work_items: List[PlanWorkItem] = []
        for work_item in work_items:
            content_object = None

            if work_item.content_type:
                model_class = work_item.content_type.model_class()
                content_object = model_class.objects.create(work_item=work_item)

            plan_work_items.append(
                PlanWorkItem(
                    plan=plan, work_item=work_item, content_object=content_object
                )
            )

        PlanWorkItem.objects.bulk_create(plan_work_items, ignore_conflicts=True)

    def create_managers(self, plan: Plan, managers: List[Manager]):
        plan_managers: List[PlanManager] = []
        for manager in managers:
            plan_managers.append(PlanManager(plan=plan, manager=manager))
        PlanManager.objects.bulk_create(plan_managers, ignore_conflicts=True)

    def create(self, validated_data):
        work_items: List[WorkItem] = validated_data.pop("work_items", [])
        managers: List[Manager] = validated_data.pop("managers", [])

        if "box_count" in validated_data and validated_data["box_count"] == 0:
            validated_data["box_count"] = None

        plan: Plan = super().create(validated_data)

        self.create_work_items(plan, work_items)
        self.create_managers(plan, managers)

        return plan

    def update(self, instance: Plan, validated_data):
        if "work_items" in validated_data:
            work_items: List[WorkItem] = validated_data.pop("work_items", [])
            PlanWorkItem.objects.filter(plan=instance).exclude(
                work_item__in=work_items
            ).delete()

            # We leave existing work_items they will cause a conflict, but we ignore it
            # and this will only create new work_items
            self.create_work_items(instance, work_items)

        if "managers" in validated_data:
            managers: List[Manager] = validated_data.pop("managers", [])
            PlanManager.objects.filter(plan=instance).exclude(
                manager__in=managers
            ).delete()

            # We leave existing work_items they will cause a conflict, but we ignore it
            # and this will only create new work_items
            self.create_managers(instance, managers)

        return super().update(instance, validated_data)

    def to_representation(self, instance: Plan):
        return PlanSerializer(
            instance, context={"request": self.context.get("request")}
        ).data


# HACK: This serializer should be declared in the clients serializer file, but
# it is declared here to avoid circular imports.
class NearbyClientSerializer(serializers.Serializer):
    """Serializer for nearby clients"""

    client = ClientSerializer()
    last_plan = PlanSerializer()
    last_shipment_plan = PlanSerializer()

    def get_last_plan(self, client) -> Optional[PlanSerializer]:
        last_plan = (
            Plan.objects.filter(client=client).order_by("-assigned_date").first()
        )

        return PlanSerializer(last_plan) if last_plan else None

    def get_last_shipment_plan(self, client) -> Optional[PlanSerializer]:
        last_shipment_plan = (
            Plan.objects.filter(client=client)
            .filter(work_items__content_type__model="shipment")
            .order_by("-assigned_date")
            .first()
        )

        return PlanSerializer(last_shipment_plan) if last_shipment_plan else None

    def to_representation(self, instance):
        data: dict[str, dict[Any, Any]] = {}

        data["client"] = ClientSerializer(instance).data

        last_plan = self.get_last_plan(instance)
        last_shipment_plan = self.get_last_shipment_plan(instance)

        if last_plan:
            data["last_plan"] = last_plan.data

        if last_shipment_plan:
            data["last_shipment_plan"] = last_shipment_plan.data

        return data
