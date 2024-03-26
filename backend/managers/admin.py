from django.contrib import admin
from managers.models import Manager


@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'last_name',
    )
    search_fields = ('first_name', 'last_name',)
    empty_value_display = '--пусто--'
    readonly_fields = (
        'created_at',
        'updated_at',
    )

    filter_horizontal = ('plans',)
