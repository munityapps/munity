from django.contrib import admin
from .models import Invite

# Invite Model
class InviteAdmin(admin.ModelAdmin):
    list_display = (
        "workspace_role",
        "email",
        "invite_token",
        "created_at",
        "updated_at",
    )
    list_filter = ("created_at",)
    fields = (
        "workspace_role",
        "email",
        "invite_token",
        "invite_estimate_timestamp_invalid",
    )

    def has_add_permission(self, request):
        return False


admin.site.register(Invite, InviteAdmin)
