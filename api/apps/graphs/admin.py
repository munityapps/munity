from django.contrib import admin
from graphs.models import Graph

# Graph Model
class GraphAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "created_at",
        "updated_at",
    )
    list_filter = ("created_at",)
    fields = (
        "name",
        "devices",
        "groups",
    )

    def has_add_permission(self, request):
        return False

admin.site.register(Graph, GraphAdmin)
