from django.contrib import admin
from managers.models import Manager, GeoPoint, Role


class ManagerRoleInline(admin.TabularInline):
    model = Manager.roles.through
    extra = 1


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "created_at",
        "updated_at",
    )
    search_fields = ("name", "created_at", "updated_at")
    empty_value_display = "--пусто--"
    readonly_fields = (
        "created_at",
        "updated_at",
    )


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
        "first_name",
        "last_name",
        "is_hidden",
        "user",
        "_roles",
    )
    search_fields = ("first_name", "last_name", "is_hidden")
    empty_value_display = "--пусто--"
    readonly_fields = (
        "created_at",
        "updated_at",
    )

    inlines = [
        ManagerRoleInline,
    ]

    def _roles(self, obj):
        return ", ".join([r.name for r in obj.roles.all()])

    _roles.short_description = "Роли"
