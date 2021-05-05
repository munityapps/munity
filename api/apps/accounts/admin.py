from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import User

# Account Model
class AccountAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "telephone",
        "social_id",
        "workspace_role_id",
        "is_active",
        "created_at",
        "updated_at",
    )
    list_filter = ("created_at",)
    fields = (
        "username",
        "email",
        "first_name",
        "last_name",
        "telephone",
        "is_active",
        "profile_picture",
        "workspace_role",
    )

    readonly_fields = [
        "profile_picture",
        "created_at",
        "updated_at",
    ]

    def has_add_permission(self, request):
        return False

    def profile_picture(self, obj):
        if obj.profile_picture_url:
            return mark_safe(
                '<img src="{url}" width="{width}" height={height} />'.format(
                    url=obj.profile_picture_url, width="60px", height="60px",
                )
            )
        return "No photo url"

admin.site.register(User, AccountAdmin)
