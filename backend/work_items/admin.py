from django.contrib import admin
from .models import BaseWorkItem, Shipment


@admin.register(BaseWorkItem)
class BaseWorkItemAdmin(admin.ModelAdmin):
    list_display = ("id", "completed_by", "work_item", "created_at", "updated_at")
    empty_value_display = "--пусто--"


@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "box_count",
        "status",
        "comment",
        "completed_by",
        "created_at",
        "updated_at",
    )
    empty_value_display = "--пусто--"
