from django.contrib import admin

from .models import Settings

# WorkspaceSettings Model
class SettingsAdmin(admin.ModelAdmin):
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

admin.site.register(Settings, SettingsAdmin)
