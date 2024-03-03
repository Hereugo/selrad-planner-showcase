from django.contrib import admin
from plans.models import Plan


class PlanInline(admin.TabularInline):
    model = Plan.managers.through
    extra = 1

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = (
        'assigned_date_formated',
        'worklist',
        'shipment_cost',
        'box_count',
        'is_completed',
        'client',
    )
    search_fields = ('client__name',)
    list_filter = ('worklist', 'is_completed', 'assigned_date',)
    empty_value_display = '--пусто--'

    readonly_fields = (
        'uuid',
        'updated_at',
        'created_at',
    )

    inlines = [
        PlanInline
    ]

    # for assignment_date also show its week day 
    def assigned_date_formated(self, obj):
        return f'{obj.assigned_date.strftime("%d %B, %Y")} ({obj.assigned_date.strftime("%A")})'
    assigned_date_formated.short_description = 'Дата назначения'
