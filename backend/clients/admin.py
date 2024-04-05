import logging
import csv
import io

from django.contrib import admin
from django.shortcuts import render, redirect
from django import forms
from django.urls import path

from leaflet.admin import LeafletGeoAdmin

from clients.models import Client, Address, ClientAddress
from api.clients.serializers import AddressSerializer
from utils.admin.mixins import ExportCsvMixin


logger = logging.getLogger(__name__)


class CsvImportForm(forms.Form):
    csv_file = forms.FileField()


@admin.action(description="Обновить координаты")
def update_coordinates(modeladmin, request, queryset):
    if queryset.count() < 1:
        modeladmin.message_user(request, "Не выбрано ни одного адреса", level="ERROR")
        return

    addresses = queryset.all()
    for address in addresses:
        address.update_coordinates()
        address.save()

    modeladmin.message_user(request, "Координаты успешно обновлены", level="SUCCESS")


@admin.action(description="Показать на карте")
def display_on_map(modeladmin, request, queryset):
    if queryset.count() < 1:
        modeladmin.message_user(request, "Не выбрано ни одного адреса", level="ERROR")
        return

    addresses = queryset.all()

    return render(
        request,
        "display_on_map.html",
        {"locations": AddressSerializer(addresses, many=True).data},
    )


@admin.action(description="Обновить координаты")
def update_coordinates_clients(modeladmin, request, queryset):
    if queryset.count() < 1:
        modeladmin.message_user(request, "Не выбрано ни одного адреса", level="ERROR")
        return

    addresses = Address.objects.filter(clients__in=queryset).all()
    for address in addresses:
        address.update_coordinates()
        address.save()

    modeladmin.message_user(request, "Координаты успешно обновлены", level="SUCCESS")


@admin.action(description="Показать на карте")
def display_on_map_client(modeladmin, request, queryset):
    if queryset.count() < 1:
        modeladmin.message_user(request, "Не выбрано ни одного клиента", level="ERROR")
        return

    addresses = Address.objects.filter(clients__in=queryset).all()

    return render(
        request,
        "display_on_map.html",
        {"locations": AddressSerializer(addresses, many=True).data},
    )


class ClientInline(admin.TabularInline):
    model = Client.addresses.through
    extra = 0
    show_change_link = True


class AddressInline(admin.TabularInline):
    model = Address.clients.through
    extra = 0
    show_change_link = True


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "plan_count",
    )
    search_fields = ("name",)
    filter_fields = ("name",)
    empty_value_display = "--пусто--"

    actions = [display_on_map_client, update_coordinates_clients]

    inlines = [
        AddressInline,
    ]

    def plan_count(self, obj):
        return obj.plans.count()

    plan_count.short_description = "Количество планов"


@admin.register(Address)
class AddressAdmin(LeafletGeoAdmin, ExportCsvMixin):
    change_list_template = "address_changelist.html"

    list_display = (
        "id",
        "street",
        "lon",
        "lat",
    )
    search_fields = ("street",)
    filter_fields = ("street",)
    empty_value_display = "--пусто--"

    inlines = [
        ClientInline,
    ]

    actions = [
        display_on_map,
        update_coordinates,
        "export_as_csv",
    ]

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path("import-csv/", self.import_csv),
        ]
        return my_urls + urls

    def import_csv(self, request):
        if request.method == "POST":
            csv_file = request.FILES["csv_file"]

            if not csv_file.name.endswith(".csv"):
                self.message_user(
                    request, "Your csv file must be in .csv format", level="ERROR"
                )
                return redirect("..")
            with io.TextIOWrapper(csv_file, encoding="utf-8", newline="\n") as file:
                reader = csv.DictReader(file)

                if (
                    "address" not in reader.fieldnames
                    or "name" not in reader.fieldnames
                ):
                    self.message_user(
                        request,
                        "Your csv file must have 'address' and 'name' columns",
                        level="ERROR",
                    )
                    return redirect("..")

                for row in reader:
                    row["address"] = row["address"].strip()
                    row["name"] = row["name"].strip()

                    client, _ = Client.objects.get_or_create(**{"name": row["name"]})

                    address, _ = Address.objects.get_or_create(
                        **{"street": row["address"]}
                    )
                    address.update_coordinates()
                    address.save()

                    ClientAddress.objects.get_or_create(
                        **{"client": client, "address": address}
                    )

            self.message_user(request, "Your csv file has been imported")
            return redirect("..")

        form = CsvImportForm()
        payload = {"form": form}
        return render(request, "csv_form.html", payload)
