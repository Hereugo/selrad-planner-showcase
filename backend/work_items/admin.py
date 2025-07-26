from django.contrib import admin

from .models import BaseWorkItem, Photo, Return, Shipment


@admin.register(BaseWorkItem)
class BaseWorkItemAdmin(admin.ModelAdmin):
    list_display = ("id", "completed_by", "work_item", "created_at", "updated_at")
    empty_value_display = "--пусто--"


@admin.register(Return)
class ReturnAdmin(BaseWorkItemAdmin):
    pass


@admin.register(Photo)
class PhotoAdmin(BaseWorkItemAdmin):
    list_display = (
        "id",
        "completed_by",
        "tg_from_chat_id",
        "tg_photo_batch_before_message_ids",
        "tg_photo_batch_after_message_ids",
        "created_at",
        "updated_at",
    )
    empty_value_display = "--пусто--"


@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "box_count",
        "status",
        "comment",
        "completed_by",
        "time_since_last_box_arrival",
        "created_at",
        "updated_at",
    )
    empty_value_display = "--пусто--"
