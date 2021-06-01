from django.contrib import admin

from .models import Log

# Log Model
class LogAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "user_id",
        "action_type",
        "modified_model_name",
        "modified_object_name",
        "modified_object_id",
        "modification",
        "name",
        "role_name",
        "workspace_name",
        "created_at",
        "updated_at",
    )
    list_filter = ("created_at",)
    fields = (
        "username",
        "name",
        "role_name",
        "workspace_name",
    )

    def has_add_permission(self, request):
        return False

admin.site.register(Log, LogAdmin)
