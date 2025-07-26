from django.contrib import admin

from managers.models import GeoPoint, Manager


@admin.register(GeoPoint)
class GeoPointAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "latitude",
        "longitude",
        "accuracy",
        "speed",
        "heading",
        "manager",
        "created_at",
    )
    search_fields = ("latitude", "longitude", "point", "manager", "created_at")
    empty_value_display = "--пусто--"
    readonly_fields = ("created_at",)


# Feature: View payment registries of a manager in a tabular form.
@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "user",
        "payment",
        "is_hidden",
        "is_manager",
        "is_driver",
        "is_warehouser",
        "is_accountant",
        "tg_user_id",
    )
    search_fields = (
        "name",
        "is_hidden",
        "is_manager",
        "is_driver",
        "is_warehouser",
        "is_accountant",
    )
    empty_value_display = "--пусто--"
