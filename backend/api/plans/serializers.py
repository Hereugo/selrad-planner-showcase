import logging
from typing import Any, Optional, List


from rest_framework import serializers
from rest_framework.request import Request
from drf_spectacular.utils import extend_schema_field
from django.utils import timezone

from api.clients.serializers import ClientSerializer
from api.users.serializers import ManagerSerializer

from clients.models import Client
from managers.models import Manager
from plans.models import Plan, WorkItem, PlanWorkItem, PlanManager, PaymentRegistry


logger = logging.getLogger(__name__)


class WorkItemSerializer(serializers.ModelSerializer):
    """Serializer for WorkItem model"""

    id = serializers.StringRelatedField()
    content_type = serializers.SerializerMethodField()

    class Meta:
        model = WorkItem
        fields = (
            "id",
            "name",
            "content_type",
        )

    @extend_schema_field(serializers.CharField)
    def get_content_type(self, obj) -> Optional[str]:
        return obj.content_type.model_class().__name__ if obj.content_type else None


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
            "invoice_date",
            "accountant_comment",
        )


class PlanCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating Plan model"""

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
    invoice_date = serializers.DateField(required=False)

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
            # Accountant stuff
            "invoice_date",
            "accountant_comment",
        )
        read_only_fields = ("id", "created_at", "updated_at")

    def validate_assigned_date(self, assigned_date):
        request: Request = self.context["request"]

        if request.user.has_perm("plans.add_old_plan"):
            return assigned_date

        if assigned_date < timezone.now().date():
            raise serializers.ValidationError(
                "У вас нет разрешения на добавление планов в прошлом"
            )

        return assigned_date

    def validate(self, attrs):
        work_items: List[WorkItem] = attrs.get("work_items", [])
        managers: List[Manager] = attrs.get("managers", [])
        work_items_name: List[str] = [
            work_item.content_type.model_class().__name__.lower()
            for work_item in work_items
            if work_item.content_type
        ]

        # If work_items contains a "shipment" type, then only one manager should be assgined as driver
        if "shipment" in work_items_name:
            drivers: List[Manager] = list(filter(lambda x: x.is_driver, managers))

            if len(drivers) > 1:
                raise serializers.ValidationError(
                    f"При наличии отгрузки, должен быть назначен только один водитель. Водители: {', '.join([d.name for d in drivers])}"
                )
            elif len(drivers) == 0:
                raise serializers.ValidationError(
                    "При наличии отгрузки, должен быть назначен хотя бы один водитель"
                )

        # Only with work_items "shipment" or "return" you can update attributes "invoice_date" or "accountant_comment"
        # if not ("shipment" in work_items_name or "return" in work_items_name):
        #     if "invoice_date" in attrs or "accountant_comment" in attrs:
        #         raise serializers.ValidationError(
        #             f"Невозможно создать/изменить атрибуты бyхгалтера без работ: отгрузка или возврат"
        #         )

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

    def create_payment_registries(self, assigned_date: timezone.datetime, managers: List[Manager]):
        payment_registries: List[PaymentRegistry] = []
        for manager in managers:
            payment_registries.append(PaymentRegistry(
                date=assigned_date,
                manager=manager,
                payment=manager.payment,
                bonus=0,
            ))

        PaymentRegistry.objects.bulk_create(payment_registries, ignore_conflicts=True)

    def create(self, validated_data):
        work_items: List[WorkItem] = validated_data.pop("work_items", [])
        managers: List[Manager] = validated_data.pop("managers", [])

        if "box_count" in validated_data and validated_data["box_count"] == 0:
            validated_data["box_count"] = None

        plan: Plan = super().create(validated_data)

        self.create_work_items(plan, work_items)
        self.create_managers(plan, managers)
        self.create_payment_registries(plan.assigned_date, managers)

        return plan

    def to_representation(self, instance: Plan):
        return PlanSerializer(
            instance, context={"request": self.context.get("request")}
        ).data


class PlanUpdateSerializer(PlanCreateSerializer):
    """Serializer for updating Plan model"""

    class Meta(PlanCreateSerializer.Meta):
        pass

    def validate_assigned_date(self, assigned_date):
        request: Request = self.context["request"]

        if request.user.has_perm("plans.change_old_plan"):
            return assigned_date

        if assigned_date < timezone.now().date():
            raise serializers.ValidationError(
                "У вас нет разрешения на изменение планов в прошлом"
            )

        return assigned_date

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

        if "assigned_date" in validated_data and validated_data.get("assigned_date") != instance.assigned_date:
            # https://stackoverflow.com/a/53321241/12423120
            # Difficult to ignore conflicts if IngerityError happens. can manually update row by row, 
            # but how do we determine which data is valid?
            # PaymentRegistry.objects.filter(date=instance.assigned_date,).update(
            #     date=validated_data.assigned_date,
            # )

            # NOTE: Not the best way, as updating the date is equivelant, except 
            # as we deleting set of date's and recreating them, we ignore all conflicts.
            # NOTE 2: ask mansur to display a warning if assigned_date is changed:
            # "WARNING: changing assigned_date results in overwritting existing payment registries, are you sure?"
            PaymentRegistry.objects.filter(date=instance.assigned_date).delete()
            managers: List[Manager] = validated_data.get("managers", instance.managers.all())
            self.create_payment_registries(validated_data.get("assigned_date"), managers)
        else:
            # NOTE: ask mansur to display a warning if managers were changed:
            # "WARNING: excluding managers results in deleting their existing payment registries, are you sure?"
            managers: List[Manager] = validated_data.get("managers", [])
            PaymentRegistry.objects.filter(date=instance.assigned_date).exclude(
                manager__in=managers
            ).delete()

            self.create_payment_registries(instance.assigned_date, managers)

        return super().update(instance, validated_data)


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
    


class PaymentRegistrySerializer(serializers.ModelSerializer):
    """Serializer for Payment Registries"""
    
    id = serializers.StringRelatedField()
    manager = ManagerSerializer(many=False)
    plans = PlanSerializer(many=True)

    class Meta:
        model = PaymentRegistry
        fields = (
            "id",
            "date",
            "manager",
            "payment",
            "bonus",
            "comment",
            "is_confirmed",
            "plans",
        )
        read_only_fields = ("id",)
    
class PaymentRegistryUpdateSerializer(serializers.ModelSerializer):
    id = serializers.StringRelatedField()

    class Meta:
        model = PaymentRegistry
        fields = (
            "id",
            "payment",
            "bonus",
            "comment",
            "is_confirmed",
        )
        read_only_fields = ("id",)

    def to_representation(self, instance: PaymentRegistry):
        return PaymentRegistrySerializer(
            instance, context={"request": self.context.get("request")}
        ).data