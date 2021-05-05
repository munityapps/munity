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

from workspace.operations import list_existing_workspaces

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
    # A handy constant for the name of the alternate database.
    workspaces = list_existing_workspaces()
    using = ""

    def group_resource_display(self, obj):
        return ", ".join([child.name for child in obj.children.all()])

    def get_db_using(self, request):
        self.using = request.META.get("HTTP_X_WORKSPACE", None)

    def save_model(self, request, obj, form, change):
        self.get_db_using(request)
        # Tell Django to save objects to the 'other' database.
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        self.get_db_using(request)
        # Tell Django to delete objects from the 'other' database
        obj.delete(using=self.using)

    def get_queryset(self, request):
        self.get_db_using(request)
        # Tell Django to look for objects on the 'other' database.
        return super().get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        self.get_db_using(request)
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super().formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        self.get_db_using(request)
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super().formfield_for_manytomany(db_field, request, using=self.using, **kwargs)


# GroupAction Model
class GroupActionAdmin(admin.ModelAdmin):
    list_display = (
        "group_action_name",
        "created_at",
        "updated_at",
    )
    list_filter = ("created_at",)
    fields = ("group_action_name",)
    # A handy constant for the name of the alternate database.
    workspaces = list_existing_workspaces()
    using = ""

    def group_resource_display(self, obj):
        return ", ".join([child.name for child in obj.children.all()])

    def get_db_using(self, request):
        self.using = request.META.get("HTTP_X_WORKSPACE", None)

    def save_model(self, request, obj, form, change):
        self.get_db_using(request)
        # Tell Django to save objects to the 'other' database.
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        self.get_db_using(request)
        # Tell Django to delete objects from the 'other' database
        obj.delete(using=self.using)

    def get_queryset(self, request):
        self.get_db_using(request)
        # Tell Django to look for objects on the 'other' database.
        return super().get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        self.get_db_using(request)
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super().formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        self.get_db_using(request)
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super().formfield_for_manytomany(db_field, request, using=self.using, **kwargs)


# GroupResource Model
class GroupResourceAdmin(admin.ModelAdmin):
    list_display = (
        "group_resource_name",
        "created_at",
        "updated_at",
    )
    list_filter = ("created_at",)
    fields = ("group_resource_name",)
    # A handy constant for the name of the alternate database.
    workspaces = list_existing_workspaces()
    using = ""

    def group_resource_display(self, obj):
        return ", ".join([child.name for child in obj.children.all()])

    def get_db_using(self, request):
        self.using = request.META.get("HTTP_X_WORKSPACE", None)

    def save_model(self, request, obj, form, change):
        self.get_db_using(request)
        # Tell Django to save objects to the 'other' database.
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        self.get_db_using(request)
        # Tell Django to delete objects from the 'other' database
        obj.delete(using=self.using)

    def get_queryset(self, request):
        self.get_db_using(request)
        # Tell Django to look for objects on the 'other' database.
        return super().get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        self.get_db_using(request)
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super().formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        self.get_db_using(request)
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super().formfield_for_manytomany(db_field, request, using=self.using, **kwargs)


# GroupRole Model
class GroupRoleAdmin(admin.ModelAdmin):
    list_display = (
        "group_role_name",
        "created_at",
        "updated_at",
    )
    list_filter = ("created_at",)
    fields = ("group_role_name",)
    # A handy constant for the name of the alternate database.
    workspaces = list_existing_workspaces()
    using = ""

    def group_resource_display(self, obj):
        return ", ".join([child.name for child in obj.children.all()])

    def get_db_using(self, request):
        self.using = request.META.get("HTTP_X_WORKSPACE", None)

    def save_model(self, request, obj, form, change):
        self.get_db_using(request)
        # Tell Django to save objects to the 'other' database.
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        self.get_db_using(request)
        # Tell Django to delete objects from the 'other' database
        obj.delete(using=self.using)

    def get_queryset(self, request):
        self.get_db_using(request)
        # Tell Django to look for objects on the 'other' database.
        return super().get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        self.get_db_using(request)
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super().formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        self.get_db_using(request)
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super().formfield_for_manytomany(db_field, request, using=self.using, **kwargs)


# WorkspaceRole Model
class WorkspaceRoleAdmin(admin.ModelAdmin):
    list_display = (
        "workspace_role_name",
        "created_at",
        "updated_at",
    )
    list_filter = ("created_at",)
    fields = ("workspace_role_name",)
    # A handy constant for the name of the alternate database.
    workspaces = list_existing_workspaces()
    using = ""

    def group_resource_display(self, obj):
        return ", ".join([child.name for child in obj.children.all()])

    def get_db_using(self, request):
        self.using = request.META.get("HTTP_X_WORKSPACE", None)

    def save_model(self, request, obj, form, change):
        self.get_db_using(request)
        # Tell Django to save objects to the 'other' database.
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        self.get_db_using(request)
        # Tell Django to delete objects from the 'other' database
        obj.delete(using=self.using)

    def get_queryset(self, request):
        self.get_db_using(request)
        # Tell Django to look for objects on the 'other' database.
        return super().get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        self.get_db_using(request)
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super().formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        self.get_db_using(request)
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super().formfield_for_manytomany(db_field, request, using=self.using, **kwargs)


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
    # A handy constant for the name of the alternate database.
    workspaces = list_existing_workspaces()
    using = ""

    def group_resource_display(self, obj):
        return ", ".join([child.name for child in obj.children.all()])

    def get_db_using(self, request):
        self.using = request.META.get("HTTP_X_WORKSPACE", None)

    def save_model(self, request, obj, form, change):
        self.get_db_using(request)
        # Tell Django to save objects to the 'other' database.
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        self.get_db_using(request)
        # Tell Django to delete objects from the 'other' database
        obj.delete(using=self.using)

    def get_queryset(self, request):
        self.get_db_using(request)
        # Tell Django to look for objects on the 'other' database.
        return super().get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        self.get_db_using(request)
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super().formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        self.get_db_using(request)
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super().formfield_for_manytomany(db_field, request, using=self.using, **kwargs)


# WorkspaceAction Model
class WorkspaceActionAdmin(admin.ModelAdmin):
    list_display = (
        "workspace_action_name",
        "created_at",
        "updated_at",
    )
    list_filter = ("created_at",)
    fields = ("workspace_action_name",)
    # A handy constant for the name of the alternate database.
    workspaces = list_existing_workspaces()
    using = ""

    def group_resource_display(self, obj):
        return ", ".join([child.name for child in obj.children.all()])

    def get_db_using(self, request):
        self.using = request.META.get("HTTP_X_WORKSPACE", None)

    def save_model(self, request, obj, form, change):
        self.get_db_using(request)
        # Tell Django to save objects to the 'other' database.
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        self.get_db_using(request)
        # Tell Django to delete objects from the 'other' database
        obj.delete(using=self.using)

    def get_queryset(self, request):
        self.get_db_using(request)
        # Tell Django to look for objects on the 'other' database.
        return super().get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        self.get_db_using(request)
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super().formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        self.get_db_using(request)
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super().formfield_for_manytomany(db_field, request, using=self.using, **kwargs)


# WorkspaceResource Model
class WorkspaceResourceAdmin(admin.ModelAdmin):
    list_display = (
        "workspace_resource_name",
        "created_at",
        "updated_at",
    )
    list_filter = ("created_at",)
    fields = ("workspace_resource_name",)
    # A handy constant for the name of the alternate database.
    workspaces = list_existing_workspaces()
    using = ""

    def group_resource_display(self, obj):
        return ", ".join([child.name for child in obj.children.all()])

    def get_db_using(self, request):
        self.using = request.META.get("HTTP_X_WORKSPACE", None)

    def save_model(self, request, obj, form, change):
        self.get_db_using(request)
        # Tell Django to save objects to the 'other' database.
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        self.get_db_using(request)
        # Tell Django to delete objects from the 'other' database
        obj.delete(using=self.using)

    def get_queryset(self, request):
        self.get_db_using(request)
        # Tell Django to look for objects on the 'other' database.
        return super().get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        self.get_db_using(request)
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super().formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        self.get_db_using(request)
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super().formfield_for_manytomany(db_field, request, using=self.using, **kwargs)


admin.site.register(GroupACL, AclAdmin)
admin.site.register(GroupAction, GroupActionAdmin)
admin.site.register(GroupResource, GroupResourceAdmin)
admin.site.register(GroupRole, GroupRoleAdmin)
admin.site.register(WorkspaceRole, WorkspaceRoleAdmin)
admin.site.register(WorkspaceACL, WorkspaceACLAdmin)
admin.site.register(WorkspaceAction, WorkspaceActionAdmin)
admin.site.register(WorkspaceResource, WorkspaceResourceAdmin)
