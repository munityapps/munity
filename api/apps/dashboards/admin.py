from django.contrib import admin
from dashboards.models import Dashboard

from workspace.operations import list_existing_workspaces


# Dashboard Model
class DashboardAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "settings",
        "created_at",
        "updated_at",
    )
    list_filter = ("created_at",)
    fields = (
        "name",
        "settings",
    )


admin.site.register(Dashboard, DashboardAdmin)
