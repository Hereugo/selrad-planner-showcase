import logging

from api.clients.serializers import AddressSerializer
from clients.models import Address, Client, MetaClient
from django.contrib import admin
from django.shortcuts import render
from leaflet.admin import LeafletGeoAdmin

logger = logging.getLogger(__name__)


@admin.action(description="Показать на карте")
def display_on_map(modeladmin, request, queryset):
    addresses = queryset.all()

    return render(
        request,
        "display_on_map.html",
        {"locations": AddressSerializer(addresses, many=True).data},
    )


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "meta_client",
        "name",
        "plan_count",
        "address",
        "is_hidden_on_map",
    )
    search_fields = ("name", "address__street")
    list_filter = ("is_hidden_on_map",)
    empty_value_display = "--пусто--"

    def plan_count(self, obj):
        return obj.plans.count()

    plan_count.short_description = "Количество планов"


class ClientInline(admin.TabularInline):
    model = Client
    extra = 0


@admin.register(MetaClient)
class MetaClientAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "client_count",
        "created_at",
    )
    empty_value_display = "--пусто--"
    inlines = [ClientInline]

    def client_count(self, obj):
        return obj.clients.count()

    client_count.short_description = "Количество магазинов"


@admin.register(Address)
class AddressAdmin(LeafletGeoAdmin):
    list_display = (
        "id",
        "street",
        "lon",
        "lat",
        "twogis_link",
        "shop_count",
    )
    search_fields = (
        "street",
        "lon",
        "lat",
    )
    empty_value_display = "--пусто--"

    actions = [
        display_on_map,
    ]
    inlines = [ClientInline]

    def shop_count(self, obj):
        return obj.clients.count()

    shop_count.short_description = "Количество магазинов"
