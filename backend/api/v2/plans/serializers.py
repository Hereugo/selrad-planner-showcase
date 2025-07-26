import logging
from typing import Optional

from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from api.v1.plans.serializers import PlanSerializer as APIv1PlanSerializer
from plans.models import PlanWorkItem

logger = logging.getLogger(__name__)


class PlanWorkItemSerializer(serializers.ModelSerializer):
    """Serializer for PlanWorkItem model"""

    task_id = serializers.StringRelatedField(source="id")
    work_item_id = serializers.StringRelatedField(source="work_item.id")
    name = serializers.CharField(source="work_item.name")
    meta_name = serializers.CharField(source="work_item.meta_name")
    content_type = serializers.SerializerMethodField()

    class Meta:
        model = PlanWorkItem
        fields = (
            "task_id",
            "work_item_id",
            "name",
            "meta_name",
            "content_type",
        )

    @extend_schema_field(serializers.CharField)
    def get_content_type(self, obj) -> Optional[str]:
        return obj.content_type.model_class().__name__ if obj.content_type else None


class PlanSerializer(APIv1PlanSerializer):
    """Serializer for Plan model"""

    work_items = PlanWorkItemSerializer(source="planworkitem_set", many=True)
