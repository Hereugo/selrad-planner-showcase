import logging
import csv
import io

from django.contrib import admin
from django.shortcuts import render, redirect
from django import forms
from django.urls import path

from leaflet.admin import LeafletGeoAdmin

from clients.models import Client, Address
from api.clients.serializers import AddressSerializer
from utils.admin.mixins import ExportCsvMixin


logger = logging.getLogger(__name__)


class CsvImportForm(forms.Form):
    csv_file = forms.FileField()


@admin.action(description="Обновить координаты по ссылке")
def update_coordinates_by_link(modeladmin, request, queryset):
    if queryset.count() == 1:
        # TODO:
        # make a separate action for a single object, providing a form for the link field
        # if no link is provided, update coordinates by the link in the object
        pass

    success_count = 0
    addresses = queryset.all()
    for address in addresses:
        try:
            address.update_coordinates_by_link()
            address.save()
            sucess_count += 1
        except Exception as e:
            logger.exception(f"Error updating coordinates: {e}")

    modeladmin.message_user(
        request,
        f"Координаты успешно обновлены для {sucess_count} из {addresses.count()}",
        level="SUCCESS",
    )


@admin.action(description="Показать на карте")
def display_on_map(modeladmin, request, queryset):
    addresses = queryset.all()

    return render(
        request,
        "display_on_map.html",
        {"locations": AddressSerializer(addresses, many=True).data},
    )


@admin.action(description="Обновить координаты по ссылке")
def update_coordinates_of_clients(modeladmin, request, queryset):
    addresses = queryset.address.all().distinct()
    return update_coordinates_by_link(modeladmin, request, addresses)


@admin.action(description="Показать на карте")
def display_on_map_client(modeladmin, request, queryset):
    addresses = queryset.address.all().distinct()
    return display_on_map(modeladmin, request, addresses)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "plan_count", "address", "is_hidden_on_map")
    search_fields = ("name", "address__street")
    list_filter = ("is_hidden_on_map",)
    empty_value_display = "--пусто--"

    actions = [display_on_map_client, update_coordinates_of_clients]

    def plan_count(self, obj):
        return obj.plans.count()

    plan_count.short_description = "Количество планов"


class ClientInline(admin.TabularInline):
    model = Client
    extra = 0


@admin.register(Address)
class AddressAdmin(LeafletGeoAdmin, ExportCsvMixin):
    change_list_template = "address_changelist.html"

    list_display = (
        "id",
        "street",
        "lon",
        "lat",
        "twogis_link",
        "is_overridden",
        "client_count",
    )
    search_fields = ("street", "lon", "lat")
    list_filter = ("is_overridden",)
    empty_value_display = "--пусто--"

    actions = [
        display_on_map,
        update_coordinates_by_link,
        "export_as_csv",
    ]
    inlines = [ClientInline]

    def client_count(self, obj):
        return obj.clients.count()

    client_count.short_description = "Количество клиентов"

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
                    or "link" not in reader.fieldnames
                ):
                    self.message_user(
                        request,
                        "Your csv file must have 'address', 'name', 'link' columns",
                        level="ERROR",
                    )
                    return redirect("..")

                # 0 - updated, 1 - created, 2 - override_dont_update_coordinates
                client_count = (0, 0)
                address_count = (0, 0, 0)
                for row in reader:
                    row["address"] = row["address"].strip()
                    row["name"] = row["name"].strip()
                    row["link"] = row["link"].strip()

                    address, is_created = Address.objects.get_or_create(
                        **{"street": row["address"]}
                    )
                    address_count[is_created] += 1
                    if not address.is_overridden:
                        address.twogis_link = row["link"]
                        address.update_coordinates_by_link(row["link"])
                    else:
                        # 2 - override_dont_update_coordinates
                        address_count[2] += 1
                    address.save()

                    client, is_created = Client.objects.get_or_create(
                        **{"name": row["name"]}
                    )
                    client_count[is_created] += 1
                    client.address = address
                    client.save()

            self.message_user(
                request,
                "<br>".join(
                    [
                        f"Клиенты: {client_count[0]} обновлены, {client_count[1]} созданы",
                        f"Адреса: {address_count[0]} обновлены, {address_count[1]} созданы, {address_count[2]} координаты не перезаписаны",
                    ]
                ),
                level="SUCCESS",
            )
            return redirect("..")

        form = CsvImportForm()
        payload = {"form": form}
        return render(request, "csv_form.html", payload)
