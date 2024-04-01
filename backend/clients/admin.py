import logging 
from django.contrib import admin
from django.shortcuts import render
from clients.models import Client, Address
from api.clients.serializers import AddressSerializer


logger = logging.getLogger(__name__)


@admin.action(description='Показать на карте')
def display_on_map(modeladmin, request, queryset):
    if queryset.count() < 1:
        modeladmin.message_user(
            request,
            'Не выбрано ни одного адреса',
            level='ERROR'
        )
        return

    addresses = queryset.all()

    return render(request, 'display_on_map.html', {
        'locations': AddressSerializer(addresses, many=True).data
    })


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'plan_count',
    )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '--пусто--'

    def plan_count(self, obj):
        return obj.plans.count()
    plan_count.short_description = 'Количество планов'


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'street',
        'lon',
        'lat',
    )
    search_fields = ('street',)
    empty_value_display = '--пусто--'

    actions = [display_on_map]
