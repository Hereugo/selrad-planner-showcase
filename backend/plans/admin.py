import logging
from django.contrib import admin
from django.shortcuts import render

from plans.models import Plan, WorkItem, Status
from managers.models import Manager

from api.plans.views import PlanViewSet


logger = logging.getLogger(__name__)


@admin.action(description="Скачать план")
def export_plans(modeladmin, request, queryset):
    if queryset.count() < 1:
        modeladmin.message_user(request, "Не выбрано ни одного плана", level="ERROR")
        return

    plans = queryset.all()

    response = PlanViewSet.export(request, plans)

    if response.status_code != 200:
        modeladmin.message_user(request, f"Не удалось скачать план", level="ERROR")
        return

    return response


@admin.action(description="Скачать отчет")
def export_report(modeladmin, request, queryset):
    plans = queryset.all()
    if "apply" in request.POST:
        response = PlanViewSet.export_report(request, request.POST["manager"], plans)

        if response.status_code != 200:
            modeladmin.message_user(request, f"Не удалось скачать отчет", level="ERROR")

        return response

    return render(
        request,
        "export_report.html",
        {
            "managers": Manager.objects.all(),
            "earliest_date": plans.earliest("assigned_date").assigned_date,
            "latest_date": plans.latest("assigned_date").assigned_date,
        },
    )


class WorkItemStatusInline(admin.TabularInline):
    model = WorkItem.statuses.through
    extra = 1


class PlanManagerInline(admin.TabularInline):
    model = Plan.managers.through
    extra = 1


class PlanWorkItemInline(admin.TabularInline):
    model = Plan.work_items.through
    extra = 1


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = (
        "assigned_date_formatted",
        "shipment_cost_formula",
        "shipment_cost",
        "box_count",
        "client",
        "client_address",
    )
    search_fields = ("client__name", "client__address", "assigned_date")
    list_filter = (
        "work_items",
        "assigned_date",
    )
    empty_value_display = "--пусто--"

    readonly_fields = (
        "updated_at",
        "created_at",
    )

    actions = [export_plans, export_report]

    inlines = [
        PlanManagerInline,
        PlanWorkItemInline,
    ]

    def client_address(self, obj):
        return obj.client.address

    client_address.short_description = "Адрес клиента"

    # for assignment_date also show its week day
    def assigned_date_formatted(self, obj):
        return f'{obj.assigned_date.strftime("%d %B, %Y")} ({obj.assigned_date.strftime("%A")})'

    assigned_date_formatted.short_description = "Дата назначения"


@admin.register(WorkItem)
class WorkItemAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
    )
    search_fields = ("name",)
    list_filter = ("name",)
    empty_value_display = "--пусто--"
    readonly_fields = (
        "updated_at",
        "created_at",
    )

    inlines = [
        WorkItemStatusInline,
    ]


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )
    search_fields = ("name",)
    list_filter = ("name",)
    empty_value_display = "--пусто--"
