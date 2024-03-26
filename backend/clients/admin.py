from django.contrib import admin
from clients.models import Client, Address


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "plan_count",
    )
    search_fields = ("name",)
    list_filter = ("name",)
    empty_value_display = "--пусто--"

    def plan_count(self, obj):
        return obj.plans.count()
    plan_count.short_description = 'Количество планов'


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = (
        "street",
        "lon",
        "lat",
    )
    search_fields = ("street",)
    empty_value_display = "--пусто--"

