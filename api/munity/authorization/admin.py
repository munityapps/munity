from django.contrib import admin

from .models import Permission, Role


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ("ressource_name", "action")

    @admin.display()
    def ressource_name(self, obj):
        return obj.ressource.model

    list_filter = ("action", "ressource")


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("name",)
