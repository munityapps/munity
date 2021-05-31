from django.contrib import admin

from .models import (
    GroupACL,
    GroupAction,
    GroupResource,
    GroupRole,
    WorkspaceRole,
    WorkspaceACL,
    WorkspaceAction,
    WorkspaceResource,
)

# Acl Model
class AclAdmin(admin.ModelAdmin):
    list_display = (
        "group_resource",
        "group_action",
        "group_role",
        "created_at",
        "updated_at",
    )
    list_filter = ("created_at",)
    fields = ()

    def group_resource_display(self, obj):
        return ", ".join([child.name for child in obj.children.all()])


# GroupAction Model
class GroupActionAdmin(admin.ModelAdmin):
    list_display = (
        "group_action_name",
        "created_at",
        "updated_at",
    )
    list_filter = ("created_at",)
    fields = ("group_action_name",)

    def group_resource_display(self, obj):
        return ", ".join([child.name for child in obj.children.all()])

# GroupResource Model
class GroupResourceAdmin(admin.ModelAdmin):
    list_display = (
        "group_resource_name",
        "created_at",
        "updated_at",
    )
    list_filter = ("created_at",)
    fields = ("group_resource_name",)

    def group_resource_display(self, obj):
        return ", ".join([child.name for child in obj.children.all()])

class GroupRoleAdmin(admin.ModelAdmin):
    list_display = (
        "group_role_name",
        "created_at",
        "updated_at",
    )
    list_filter = ("created_at",)
    fields = ("group_role_name",)

    def group_resource_display(self, obj):
        return ", ".join([child.name for child in obj.children.all()])

class WorkspaceRoleAdmin(admin.ModelAdmin):
    list_display = (
        "workspace_role_name",
        "created_at",
        "updated_at",
    )
    list_filter = ("created_at",)
    fields = ("workspace_role_name",)

    def group_resource_display(self, obj):
        return ", ".join([child.name for child in obj.children.all()])

# WorkspaceACL Model
class WorkspaceACLAdmin(admin.ModelAdmin):
    list_display = (
        "workspace_role",
        "workspace_action",
        "workspace_resource",
        "created_at",
        "updated_at",
    )
    list_filter = ("created_at",)
    fields = (
        "workspace_role",
        "workspace_action",
        "workspace_resource",
    )

    def group_resource_display(self, obj):
        return ", ".join([child.name for child in obj.children.all()])

class WorkspaceActionAdmin(admin.ModelAdmin):
    list_display = (
        "workspace_action_name",
        "created_at",
        "updated_at",
    )
    list_filter = ("created_at",)
    fields = ("workspace_action_name",)

    def group_resource_display(self, obj):
        return ", ".join([child.name for child in obj.children.all()])

class WorkspaceResourceAdmin(admin.ModelAdmin):
    list_display = (
        "workspace_resource_name",
        "created_at",
        "updated_at",
    )
    list_filter = ("created_at",)
    fields = ("workspace_resource_name",)

    def group_resource_display(self, obj):
        return ", ".join([child.name for child in obj.children.all()])

admin.site.register(GroupACL, AclAdmin)
admin.site.register(GroupAction, GroupActionAdmin)
admin.site.register(GroupResource, GroupResourceAdmin)
admin.site.register(GroupRole, GroupRoleAdmin)
admin.site.register(WorkspaceRole, WorkspaceRoleAdmin)
admin.site.register(WorkspaceACL, WorkspaceACLAdmin)
admin.site.register(WorkspaceAction, WorkspaceActionAdmin)
admin.site.register(WorkspaceResource, WorkspaceResourceAdmin)
