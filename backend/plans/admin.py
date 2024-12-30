import logging

from django.contrib import admin
from django.shortcuts import render
from django.db.models import QuerySet

from plans.models import Plan, WorkItem, PaymentRegistry
from managers.models import Manager

from api.plans.views import PlanViewSet


logger = logging.getLogger(__name__)

@admin.action(description="Unfix plan")
def unfix_plans(modeladmin, request, queryset):
    if queryset.count() < 1:
        modeladmin.message_user(request, "Не выбрано ни одного плана", level="ERROR")
        return

    plans: QuerySet[Plan] = queryset.all()
    count = plans.update(is_permanent=False)

    modeladmin.message_user(request, f"{count} план(ов) были изменины из перманентный")
    return

    
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


class PlanManagerInline(admin.TabularInline):
    model = Plan.managers.through
    extra = 1


class PlanWorkItemInline(admin.TabularInline):
    model = Plan.work_items.through
    extra = 1


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = (
        "is_permanent",
        "assigned_date_formatted",
        "shipment_cost_formula",
        "shipment_cost",
        "box_count",
        "client",
        "client_address",
        "time_since_first_dispatch",
        "invoice_date",
        "accountant_comment",
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

    actions = [export_plans, export_report, unfix_plans]

    inlines = [
        PlanManagerInline,
        PlanWorkItemInline,
    ]

    def client_address(self, obj):
        return obj.client.address

    client_address.short_description = "Адрес магазина"

    # for assignment_date also show its week day
    def assigned_date_formatted(self, obj):
        return f'{obj.assigned_date.strftime("%d %B, %Y")} ({obj.assigned_date.strftime("%A")})'

    assigned_date_formatted.short_description = "Дата назначения"


@admin.register(WorkItem)
class WorkItemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "content_type",
        "created_at",
    )
    search_fields = ("name", "content_type__model")
    empty_value_display = "--пусто--"
    readonly_fields = ("created_at",)


@admin.register(PaymentRegistry)
class PaymentRegistryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "is_confirmed",
        "date",
        "manager",
        "payment",
        "bonus",
        "plans_count",
    )
    list_filter = (
        "is_confirmed",
        "date",
        "manager",
    )
    empty_value_display = "--пусто--"

    def plans_count(self, obj):
        return obj.plans().count()

    plans_count.short_description = "Кол-во планов"
