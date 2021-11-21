import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import SET_NULL
from django_extensions.db.models import TimeStampedModel

from ..models import MunityGroupableModel

class User(AbstractUser, TimeStampedModel, MunityGroupableModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    def get_absolute_url(self):
        return f"/users/{self.id}"

class UserRoleWorkspace(TimeStampedModel):
    user = models.ForeignKey("users.User", related_name="user_role_workspaces", on_delete=models.CASCADE)
    workspace = models.ForeignKey("workspaces.Workspace", on_delete=models.CASCADE, null=True)
    role = models.ForeignKey("authorization.Role", on_delete=models.CASCADE)

    class Meta:
        unique_together=('user', 'workspace')

class UserRoleGenericGroup(TimeStampedModel):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    group = models.ForeignKey("generic_groups.GenericGroup", on_delete=models.CASCADE)
    role = models.ForeignKey("authorization.Role", on_delete=models.CASCADE)

    class Meta:
        unique_together=('user', 'group')
