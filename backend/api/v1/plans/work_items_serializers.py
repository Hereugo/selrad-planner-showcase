# Description: Serializers for work items models.
# Note each work item serializer must have "work_item" field
# since PolyMorphicModelSerializer uses this field to determine the model type.

import logging
from typing import Any

from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from rest_polymorphic.serializers import PolymorphicSerializer

from api.v1.plans.serializers import PlanSerializer, WorkItemSerializer
from managers.models import Manager
from plans.models import PlanWorkItem
from work_items.models import BaseWorkItem, Photo, Return, Shipment

logger = logging.getLogger(__name__)


class BaseWorkItemSerializer(serializers.ModelSerializer):
    id = serializers.StringRelatedField()
    work_item = serializers.StringRelatedField()
    completed_by = serializers.CharField(source="completed_by.name", allow_null=True)

    class Meta:
        model = BaseWorkItem
        fields = (
            "id",
            "completed_by",
            "work_item",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "work_item",
            "created_at",
            "updated_at",
        )


class BaseWorkItemUpdateSerializer(serializers.ModelSerializer):
    completed_by = serializers.PrimaryKeyRelatedField(
        queryset=Manager.objects.all(),
        required=False,
    )

    class Meta:
        model = BaseWorkItem
        fields = ("completed_by",)

    # def validate(self, attrs):
    #     manager = self.context["request"].user.manager
    #     if "completed_by" in attrs and attrs["completed_by"] != manager:
    #         raise serializers.ValidationError(
    #             f"You can't update from another manager, received manager {attrs['completed_by']} but expected {manager}"
    #         )
    #
    #     return super().validate(attrs)

    def to_representation(self, instance):
        return BaseWorkItemSerializer(instance).data


class PhotoSerializer(BaseWorkItemSerializer):
    """Serializer for Photo model"""

    tg_photo_batch_before_message_ids = serializers.JSONField(allow_null=True)
    tg_photo_batch_after_message_ids = serializers.JSONField(allow_null=True)
    tg_from_chat_id = serializers.IntegerField(allow_null=True)

    class Meta(BaseWorkItemSerializer.Meta):
        model = Photo
        fields = BaseWorkItemSerializer.Meta.fields + (
            "tg_photo_batch_before_message_ids",
            "tg_photo_batch_after_message_ids",
            "tg_from_chat_id",
        )


class PhotoUpdateSerializer(BaseWorkItemUpdateSerializer):
    """Serializer for Photo model"""

    tg_photo_batch_before_message_ids = serializers.JSONField(allow_null=True)
    tg_photo_batch_after_message_ids = serializers.JSONField(allow_null=True)
    tg_from_chat_id = serializers.IntegerField(allow_null=True)

    class Meta(BaseWorkItemUpdateSerializer.Meta):
        model = Photo
        fields = BaseWorkItemUpdateSerializer.Meta.fields + (
            "tg_photo_batch_before_message_ids",
            "tg_photo_batch_after_message_ids",
            "tg_from_chat_id",
        )


class ShipmentSerializer(BaseWorkItemSerializer):
    """Serializer for Shipment model"""

    status_choices = serializers.SerializerMethodField()

    box_count = serializers.IntegerField(allow_null=True)
    status = serializers.CharField(allow_null=True)
    comment = serializers.CharField(allow_null=True)

    class Meta(BaseWorkItemSerializer.Meta):
        model = Shipment
        fields = BaseWorkItemSerializer.Meta.fields + (
            "box_count",
            "status",
            "status_choices",
            "comment",
        )

    @extend_schema_field(serializers.DictField)
    def get_status_choices(self, obj) -> dict[str, Any]:
        return dict(Shipment.CHOICES)


class ShipmentUpdateSerializer(BaseWorkItemUpdateSerializer):
    """Serializer for Shipment model"""

    status = serializers.ChoiceField(
        allow_null=True, choices=Shipment.CHOICES, required=False
    )

    class Meta(BaseWorkItemUpdateSerializer.Meta):
        model = Shipment
        fields = BaseWorkItemUpdateSerializer.Meta.fields + (
            "box_count",
            "status",
            "comment",
        )

    def to_representation(self, instance):
        return ShipmentSerializer(instance).data


class ReturnSerializer(BaseWorkItemSerializer):
    class Meta(BaseWorkItemSerializer.Meta):
        modal = Return


class ReturnUpdateSerializer(BaseWorkItemUpdateSerializer):
    class Meta(BaseWorkItemUpdateSerializer.Meta):
        modal = Return


class WorkItemPolymorphicSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        BaseWorkItem: BaseWorkItemSerializer,
        Shipment: ShipmentSerializer,
        Return: ReturnSerializer,
        Photo: PhotoSerializer,
    }


class TaskSerializer(serializers.ModelSerializer):
    id = serializers.StringRelatedField()
    plan = PlanSerializer()
    work_item = WorkItemSerializer()
    content = serializers.SerializerMethodField()

    class Meta:
        model = PlanWorkItem
        fields = (
            "id",
            "plan",
            "work_item",
            "content",
        )

    @extend_schema_field(WorkItemPolymorphicSerializer)
    def get_content(self, obj):
        return WorkItemPolymorphicSerializer(obj.content_object).data


class TaskUpdatePolymorphicSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        BaseWorkItem: BaseWorkItemUpdateSerializer,
        Shipment: ShipmentUpdateSerializer,
        Return: ReturnUpdateSerializer,
        Photo: PhotoUpdateSerializer,
    }
