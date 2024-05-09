from rest_framework import serializers
from clients.models import Client, Address
from plans.models import Plan


class AddressSerializer(serializers.ModelSerializer):
    """Serializer for Address model"""

    id = serializers.StringRelatedField()
    lon = serializers.FloatField()
    lat = serializers.FloatField()

    class Meta:
        model = Address
        fields = (
            "id",
            "street",
            "lon",
            "lat",
            "created_at",
            "updated_at",
        )


class ClientSerializer(serializers.ModelSerializer):
    """Serializer for Client model"""

    id = serializers.StringRelatedField()
    address = AddressSerializer(read_only=True, many=False)

    class Meta:
        model = Client
        fields = (
            "id",
            "name",
            "created_at",
            "updated_at",
            "address",
            "is_hidden_on_map",
        )


class NearbyClientSerializer(serializers.ModelSerializer):
    """Serializer for Client model"""

    id = serializers.StringRelatedField()
    address = AddressSerializer(read_only=True, many=False)

    class Meta:
        model = Client
        fields = (
            "id",
            "name",
            "created_at",
            "updated_at",
            "address",
            "is_hidden_on_map",
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)

        plan_pk = self.context.get("plan_pk")
        plan = Plan.objects.filter(pk=plan_pk).first()

        latest_plan = instance.plans.filter(
            assigned_date__lte=plan.assigned_date
        ).latest("assigned_date")

        if latest_plan:
            data["assigned_date_diff"] = plan.assigned_date - latest_plan.assigned_date
        else:
            data["assigned_date_diff"] = -1

        return data
