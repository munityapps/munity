import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import SET_NULL

from munity.authorization.models import Role
from ..models import MunityGroupableModel, MunityModel

class User(AbstractUser, MunityModel, MunityGroupableModel):
    roles = models.ManyToManyField("authorization.Role", through="UserRoleWorkspace", related_name="roles")
    def get_absolute_url(self):
        return f"/users/{self.id}"

class UserRoleWorkspace(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    workspace = models.ForeignKey("workspaces.Workspace", on_delete=models.CASCADE, null=True)
    role = models.ForeignKey("authorization.Role", on_delete=models.CASCADE)

    class Meta:
        unique_together=('user', 'workspace', 'role')

class UserRoleGenericGroup(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    group = models.ForeignKey("generic_groups.GenericGroup", on_delete=models.CASCADE)
    role = models.ForeignKey("authorization.Role", on_delete=models.CASCADE)

    class Meta:
        unique_together=('user', 'group', 'role')
