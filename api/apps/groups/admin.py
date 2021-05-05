from django.contrib import admin
from groups.models import Group

# Group Model
class GroupAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "created_at",
        "updated_at",
    )
    list_filter = ("created_at",)
    fields = ("name",)

    def has_add_permission(self, request):
        return False


admin.site.register(Group, GroupAdmin)
