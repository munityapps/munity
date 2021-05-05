import uuid

from django.db import models
from django.db.models import JSONField
from django.db.models.signals import post_delete, post_save, pre_delete, pre_save
from django.dispatch import receiver

from acl.models import GroupRole, WorkspaceRole
from base.operations import get_modification
from groups.models import Group
from outputs.models import Log
from base.operations import update_or_delete_custom_field


class Invite(models.Model):
    """
    An Invite.
    """

    class Meta:
        ordering = ("email",)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    workspace_role = models.ForeignKey(
        WorkspaceRole,
        on_delete=models.SET_NULL,
        related_name="invitees",
        verbose_name="This invitees's potential role in the Workspace.",
        null=True,
    )
    email = models.CharField(max_length=64, blank=True)
    invite_token = models.CharField(max_length=1000, unique=True)
    invite_estimate_timestamp_invalid = models.PositiveIntegerField()
    groups = models.ManyToManyField(
        Group,
        related_name="potential_members",
        through="InviteGroupMembership",
        through_fields=("invite", "group", "custom_field"),
    )
    custom_field = JSONField(null=False, blank=True, default=dict)

    def get_associated_groups(self):
        """This function is required for ACL's. It returns the list of groups this invitee belongs to."""
        return self.groups.all()

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.email} >"


class InviteGroupMembership(models.Model):
    class Meta:
        unique_together = ("invite", "group")

    invite_group_membership_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    invite = models.ForeignKey(Invite, related_name="invite_group_memberships", on_delete=models.CASCADE)
    group = models.ForeignKey(Group, related_name="invite_group_memberships", on_delete=models.CASCADE)
    group_role = models.ForeignKey(
        GroupRole, related_name="invite_group_memberships_with_role", on_delete=models.CASCADE
    )

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.invite_id} - {self.id} ({self.group_role_id})>"

    def get_associated_groups(self, invite_id):
        """This function is required for ACL's. It returns the list of groups this device belongs to."""
        return Group.objects.filter(invite_group_memberships__invite_id=invite_id)


# Log Activity
@receiver(pre_save, sender=Invite)
@receiver(pre_delete, sender=Invite)
def get_old(sender, instance, **kwargs):
    try:
        instance.old = Invite.objects.get(pk=instance.pk)
    except Invite.DoesNotExist:
        instance.old = None


@receiver(post_save, sender=Invite)
def add_invite(sender, instance, created, **kwargs):
    action_type = "CREATE" if created else "UPDATE"
    model_fields = Invite._meta.get_fields()
    old = instance.old
    del instance.old
    new = instance

    log = Log(
        action_type=action_type,
        modified_model_name="Invite",
        modified_object_name=instance.email,
        modified_object_id=instance.id,
        role_name=instance.workspace_role.workspace_role_name if instance.workspace_role else None,
        modification=get_modification(old, new, model_fields, action_type),
    ).save()


@receiver(post_delete, sender=Invite)
def delete_invite(sender, instance, using, **kwargs):
    action_type = "REMOVE"
    model_fields = Invite._meta.get_fields()
    log = Log(
        action_type=action_type,
        modified_model_name="Invite",
        modified_object_name=instance.email,
        modified_object_id=instance.id,
        role_name=instance.workspace_role.workspace_role_name if instance.workspace_role else None,
        modification=get_modification(instance, None, model_fields, action_type),
    ).save()


@receiver(post_save, sender=InviteGroupMembership)
def add_invite_group_membership(sender, instance, created, **kwargs):
    action_type = "ADD TO GROUP"
    log = Log(
        action_type=action_type,
        modified_model_name="InviteGroupMembership",
        modified_object_name=instance.invite.email,
        modified_object_id=instance.pk,
        name=instance.group.name,
        role_name=instance.group_role.group_role_name,
    ).save()


@receiver(post_delete, sender=InviteGroupMembership)
def remove_invite_group_membership(sender, instance, **kwargs):
    action_type = "REMOVE FROM GROUP"
    log = Log(
        action_type=action_type,
        modified_model_name="InviteGroupMembership",
        modified_object_name=instance.invite.email,
        modified_object_id=instance.pk,
        name=instance.group.name,
        role_name=instance.group_role.group_role_name,
    ).save()


@receiver(pre_save, sender=Invite)
def update_or_delete_user_custom_field(sender, instance, using, **kwargs):
    if not instance._state.adding:
        current_device = Invite.objects.using(using).get(pk=instance.id)
        update_or_delete_custom_field(current_device, instance)
