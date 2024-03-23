from rest_framework import serializers 
from plans.models import Plan, Worklist

from clients.serializers import ClientShortSerializer, AddressSerializer
from managers.serializers import ManagerSerializer


class WorklistSerializer(serializers.ModelSerializer):
    """Serializer for Worklist model"""
    class Meta:
        model = Worklist
        fields = (
            'pk',
            'name',
            'description',
            'created_at',
            'updated_at',
        )


class PlanSerializer(serializers.ModelSerializer):
    """Serializer for Plan model"""
    worklist = WorklistSerializer(many=True)
    client = ClientShortSerializer()
    address = AddressSerializer()
    managers = ManagerSerializer(many=True)

    class Meta:
        model = Plan 
        fields = (
            'pk',
            'assigned_date',
            'worklist',
            'client',
            'address',
            'shipment_cost',
            'comment',
            'managers',
            'box_count',
            'created_at',
            'updated_at',
        )
