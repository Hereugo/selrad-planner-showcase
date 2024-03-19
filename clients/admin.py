from django.contrib import admin
from clients.models import Client, Address


class ClientInline(admin.TabularInline):
    model = Client.addresses.through
    extra = 0


class AddressInline(admin.TabularInline):
    model = Address.clients.through
    extra = 0


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "plan_count",
    )
    search_fields = ("name",)
    list_filter = ("name",)
    empty_value_display = "--пусто--"

    inlines = [
        AddressInline,
    ]

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
    search_fields = ("name",)
    list_filter = ("client",)
    empty_value_display = "--пусто--"

    inlines = [
        ClientInline,
    ]
