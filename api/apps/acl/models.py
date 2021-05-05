import uuid

from django.db import models


class WorkspaceRole(models.Model):
    class Meta:
        ordering = ("workspace_role_name",)

    workspace_role_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    workspace_role_name = models.CharField(max_length=64, unique=True)

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.workspace_role_name}>"

    def __str__(self):
        return f"{self.workspace_role_name}"


class WorkspaceAction(models.Model):
    class Meta:
        ordering = ("workspace_action_name",)

    workspace_action_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    workspace_action_name = models.CharField(max_length=64, unique=True)

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.workspace_action_name}>"

    def __str__(self):
        return f"{self.workspace_action_name}"


class WorkspaceResource(models.Model):
    class Meta:
        ordering = ("workspace_resource_name",)

    workspace_resource_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    workspace_resource_name = models.CharField(max_length=64, unique=True)

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.workspace_resource_name}>"

    def __str__(self):
        return f"{self.workspace_resource_name}"


class WorkspaceACL(models.Model):
    class Meta:
        unique_together = ("workspace_role", "workspace_action", "workspace_resource")

    workspace_acl_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    workspace_role = models.ForeignKey(WorkspaceRole, on_delete=models.CASCADE)
    workspace_action = models.ForeignKey(WorkspaceAction, on_delete=models.CASCADE)
    workspace_resource = models.ForeignKey(WorkspaceResource, on_delete=models.CASCADE)

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.workspace_role.workspace_role_name} {self.workspace_action.workspace_action_name} {self.workspace_resource.workspace_resource_name}>"

    def __str__(self):
        return f"{self.workspace_resource.workspace_resource_name}"


class GroupRole(models.Model):
    class Meta:
        ordering = ("group_role_name",)

    group_role_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    group_role_name = models.CharField(max_length=64, unique=True)

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.group_role_name}>"

    def __str__(self):
        return f"{self.group_role_name}"


class GroupAction(models.Model):
    class Meta:
        ordering = ("group_action_name",)

    group_action_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    group_action_name = models.CharField(max_length=64, unique=True)

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.group_action_name}>"

    def __str__(self):
        return f"{self.group_action_name}"


class GroupResource(models.Model):
    class Meta:
        ordering = ("group_resource_name",)

    group_resource_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    group_resource_name = models.CharField(max_length=64, unique=True)

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.group_resource_name}>"

    def __str__(self):
        return f"{self.group_resource_name}"


class GroupACL(models.Model):
    class Meta:
        unique_together = ("group_role", "group_action", "group_resource")

    group_acl_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    group_role = models.ForeignKey(GroupRole, on_delete=models.CASCADE)
    group_action = models.ForeignKey(GroupAction, on_delete=models.CASCADE)
    group_resource = models.ForeignKey(GroupResource, on_delete=models.CASCADE)

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.group_role.group_role_name} {self.group_action.group_action_name} {self.group_resource.group_resource_name}>"
