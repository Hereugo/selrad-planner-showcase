import logging

from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field

from api.clients.serializers import ClientSerializer, AddressSerializer
from api.managers.serializers import ManagerSerializer

from clients.models import Client, Address
from managers.models import Manager
from plans.models import Plan, Worklist, PlanWorklist, PlanManager


logger = logging.getLogger(__name__)


class WorklistSerializer(serializers.ModelSerializer):
    """Serializer for Worklist model"""

    class Meta:
        model = Worklist
        fields = (
            "id",
            "name",
            "description",
            "created_at",
            "updated_at",
        )


class PlanSerializer(serializers.ModelSerializer):
    """Serializer for Plan model"""

    worklist = WorklistSerializer(many=True)
    client = ClientSerializer()
    managers = ManagerSerializer(many=True)
    box_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Plan
        fields = (
            "id",
            "assigned_date",
            "worklist",
            "client",
            "shipment_cost",
            "comment",
            "managers",
            "box_count",
            "created_at",
            "updated_at",
        )


class PlanUpdateSerializer(serializers.ModelSerializer):
    """Serializer for Plan model"""

    worklist = serializers.PrimaryKeyRelatedField(
        queryset=Worklist.objects.all(),
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
    box_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Plan
        fields = (
            "id",
            "assigned_date",
            "worklist",
            "client",
            "shipment_cost",
            "comment",
            "managers",
            "box_count",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "box_count", "created_at", "updated_at")

    def create_worklist(self, plan, worklist):
        plan_worklist = []
        for w in worklist:
            plan_worklist.append(PlanWorklist(plan=plan, worklist=w))
        print(plan_worklist)

        PlanWorklist.objects.bulk_create(plan_worklist, ignore_conflicts=True)

    def create_managers(self, plan, managers):
        plan_managers = []
        for manager in managers:
            plan_managers.append(PlanManager(plan=plan, manager=manager))
        PlanManager.objects.bulk_create(plan_managers, ignore_conflicts=True)

    def create(self, validated_data):
        worklist = validated_data.pop("worklist", [])
        managers = validated_data.pop("managers", [])

        plan = super().create(validated_data)

        self.create_worklist(plan, worklist)
        self.create_managers(plan, managers)

        return plan

    def update(self, instance, validated_data):
        PlanWorklist.objects.filter(plan=instance).delete()
        PlanManager.objects.filter(plan=instance).delete()

        if "worklist" in validated_data:
            worklist = validated_data.pop("worklist", [])
            self.create_worklist(instance, worklist)

        if "managers" in validated_data:
            managers = validated_data.pop("managers", [])
            self.create_managers(instance, managers)

        return super().update(instance, validated_data)

    def to_representation(self, instance):
        return PlanSerializer(
            instance, context={"request": self.context.get("request")}
        ).data


class MapSerializer(serializers.ModelSerializer):
    """Serializer for Plan model"""

    date = serializers.SerializerMethodField()
    data = serializers.SerializerMethodField()
    color = serializers.SerializerMethodField()

    @extend_schema_field(serializers.CharField())
    def get_color(self, obj):
        return "#0000FF"  # later changed in view

    @extend_schema_field(serializers.DateField())
    def get_date(self, obj):
        return obj.assigned_date

    @extend_schema_field(PlanSerializer(many=True))
    def get_data(self, obj):
        plans = Plan.objects.filter(assigned_date=obj.assigned_date)
        return PlanSerializer(plans, many=True).data

    class Meta:
        model = Plan
        fields = ("date", "data", "color")
