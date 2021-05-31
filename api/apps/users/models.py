import uuid

from django.db.models import JSONField
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_delete, post_save, pre_delete, pre_save
from django.dispatch import receiver

from acl.models import GroupRole, WorkspaceRole
from base.operations import get_modification
from groups.models import Group
from base.operations import update_or_delete_custom_field


class User(AbstractUser):
    """
    This is a custom User class that inherits from Django's AbstractUser, which in turn inherits from AbstractBaseUser:
    https://docs.djangoproject.com/en/2.1/topics/auth/customizing/#django.contrib.auth.models.AbstractBaseUser"""

    class Meta:
        ordering = ("username",)

    # auth fields
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    social_id = models.CharField(db_index=True, max_length=128, blank=True, default="")

    # information fields
    profile_picture_url = models.URLField(default=None, null=True)
    telephone = models.CharField(max_length=128, blank=True, null=True)
    preferred_language = models.CharField(default="en", blank=True, max_length=8)
    custom_field = JSONField(null=False, blank=True, default=dict)

    user_permissions = None

    # rights fields
    workspace_role = models.ForeignKey(
        WorkspaceRole,
        on_delete=models.SET_NULL,
        related_name="users",
        verbose_name="This user's role in the Workspace.",
        null=True,
    )
    groups = models.ManyToManyField(
        # This ManyToManyField is defined on this side of the relation because AbstractUser already has a
        # ManyToManyField pointing to django.contrib.auth.models.Group, and we need to redefine it.
        Group,
        related_name="members",
        through="UserGroupMembership",
        through_fields=("user", "group"),
    )

    # misc fields
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.username}>"

    def get_associated_groups(self, user_id):
        """This function is required for ACL's. It returns the list of groups this user belongs to."""
        return Group.objects.filter(group_memberships__user_id=user_id)


class UserGroupMembership(models.Model):
    class Meta:
        unique_together = ("user", "group")

    user_group_membership_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    user = models.ForeignKey(User, related_name="group_memberships", on_delete=models.CASCADE)
    group = models.ForeignKey(Group, related_name="group_memberships", on_delete=models.CASCADE)
    group_role = models.ForeignKey(GroupRole, related_name="group_memberships_with_role", on_delete=models.CASCADE)

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.user_id} - {self.id} ({self.group_role_id})>"

    def get_associated_groups(self, user_id):
        """This function is required for ACL's. It returns the list of groups this device belongs to."""
        return Group.objects.filter(group_memberships__user_id=user_id)


# Log Activity
@receiver(pre_save, sender=User)
@receiver(pre_delete, sender=User)
def get_old(sender, instance, using, **kwargs):
    workspace_slug = instance._state.db
    try:
        instance.old = User.objects.using(workspace_slug).get(id=instance.id)
    except User.DoesNotExist:
        instance.old = None


@receiver(post_save, sender=User)
def add_user(sender, instance, created, using, update_fields, **kwargs):
    from outputs.models import Log

    action_type = "CREATE" if created else "UPDATE"

    if update_fields and "is_active" in update_fields:
        action_type = "ACTIVATE"

    model_fields = User._meta.get_fields()
    old = instance.old
    del instance.old
    new = instance

    # To prevent save meaningless Log when `ADD TO GROUP` or `REMOVE FROM GROUP`
    modification = get_modification(old, new, model_fields, action_type)
    if modification:
        Log(
            action_type=action_type,
            modified_model_name="User",
            modified_object_name=instance.email,
            modified_object_id=instance.id,
            role_name=instance.workspace_role.workspace_role_name if instance.workspace_role else None,
            username=instance.email,
            user_id=instance.id,
            workspace_name=using,
            modification=modification,
        ).save(using=using)


@receiver(post_delete, sender=User)
def delete_user(sender, instance, using, **kwargs):
    from outputs.models import Log

    action_type = "REMOVE"
    model_fields = User._meta.get_fields()
    log = Log(
        action_type=action_type,
        modified_model_name="User",
        modified_object_name=instance.email,
        modified_object_id=instance.id,
        role_name=instance.workspace_role.workspace_role_name if instance.workspace_role else None,
        modification=get_modification(instance, None, model_fields, action_type),
    )
    log.save()


@receiver(post_save, sender=UserGroupMembership)
def add_user_group_membership(sender, instance, created, **kwargs):
    from outputs.models import log_group_relation_changes

    log_group_relation_changes(
        "UserGroupMembership",
        instance.user.email,
        instance.user.id,
        "post_add",
        [instance.group.id],
        instance.group_role.group_role_name,
    )


@receiver(post_delete, sender=UserGroupMembership)
def remove_user_group_membership(sender, instance, **kwargs):
    from outputs.models import log_group_relation_changes

    log_group_relation_changes(
        "UserGroupMembership",
        instance.user.email,
        instance.user.id,
        "post_remove",
        [instance.group.id],
        instance.group_role.group_role_name,
    )


@receiver(pre_save, sender=User)
def update_or_delete_user_custom_field(sender, instance, using, **kwargs):
    if not instance._state.adding:
        workspace_slug = instance._state.db
        current_device = User.objects.using(workspace_slug).get(pk=instance.id)
        update_or_delete_custom_field(current_device, instance)
