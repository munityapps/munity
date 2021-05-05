from django.contrib import admin

from workspace.models import WorkspaceSettings

# WorkspaceSettings Model
class WorkspaceSettingsAdmin(admin.ModelAdmin):
    list_display = (
        "key",
        "value",
        "created_at",
        "updated_at",
    )
    list_filter = ("created_at",)
    fields = (
        "key",
        "value",
    )

admin.site.register(WorkspaceSettings, WorkspaceSettingsAdmin)
