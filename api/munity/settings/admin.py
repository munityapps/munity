from django.contrib import admin
from .models import Settings

@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ("key", "value", "workspace")
    list_editable = ("value",)
    list_filter = ("key", "workspace")