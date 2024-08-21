from django.contrib import admin
from managers.models import Manager, GeoPoint


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


@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "user",
        "is_hidden",
        "is_manager",
        "is_driver",
        "is_keeper",
    )
    search_fields = (
        "name",
        "last_name",
        "is_hidden",
        "is_manager",
        "is_driver",
        "is_keeper",
    )
    empty_value_display = "--пусто--"
