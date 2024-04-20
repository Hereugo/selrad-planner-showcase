from django.contrib import admin
from managers.models import Manager


@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "is_hidden",
    )
    search_fields = ("first_name", "last_name", "is_hidden")
    empty_value_display = "--пусто--"
    readonly_fields = (
        "created_at",
        "updated_at",
    )
