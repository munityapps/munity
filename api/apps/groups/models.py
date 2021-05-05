import uuid

from django.db.models import JSONField
from django.db import models
from django.db.models.signals import post_delete, post_save, pre_delete, pre_save
from django.dispatch import receiver

from base.operations import get_modification
from base.operations import update_or_delete_custom_field

DROP_FIELD_LOG = ["updated_at"]


class Group(models.Model):
    """
    A Group. Contains Users and Devices.
    """

    class Meta:
        ordering = ("name",)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64, unique=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    groups = models.ManyToManyField("self", related_name="group+", symmetrical=False, blank=True)

    custom_field = JSONField(null=False, blank=True, default=dict)

    def get_associated_groups(self):
        """This function is required for ACL's. Returns a list containing itself."""
        return [self]

    def get_all_groups(self):
        """get all groups in a group"""
        return self.groups.all()

    def get_related_devices(self):

        # Get related groups of self
        groups_related = self.get_related_groups()
        # Append self if not already in groups_related
        if self not in groups_related:
            groups_related.append(self)
        devices_related = []
        # Get all devices of groups related
        for group in groups_related:
            for device in group.devices.all():
                if device not in devices_related:
                    devices_related.append(device)

        return devices_related

    def get_related_users(self):

        # Get related groups of self
        groups_related = self.get_related_groups()
        # Append self if not already in groups_related
        if self not in groups_related:
            groups_related.append(self)
        users_related = []
        # Get all devices of groups related
        for group in groups_related:
            for user in group.members.all():
                if user not in users_related:
                    users_related.append(user)
        return users_related

    def get_related_groups(self, container=None):
        """
            get Devices Related from a group
        """
        if container is None:
            container = []
        groups_related = container
        for group in self.get_all_groups():
            groups_related.append(group)
            for group_child in group.get_all_groups():
                if group_child not in groups_related:
                    group_child.get_related_groups(groups_related)

        return groups_related

    def __contains__(self, obj):
        """Special python method that allows us to use the `in` keyword"""

        if obj.__class__.__name__ in ("Device", "User"):
            return self in obj.groups.all()

        elif obj.__class__.__name__ == "Graph":
            return self == obj.group

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.name}>"

    def __str__(self):
        return f"{self.name}"


# Log Activity
@receiver(pre_save, sender=Group)
@receiver(pre_delete, sender=Group)
def get_old(sender, instance, **kwargs):
    try:
        instance.old = Group.objects.get(pk=instance.pk)
    except Group.DoesNotExist:
        instance.old = None


@receiver(post_save, sender=Group)
def add_group(sender, instance, created, **kwargs):
    from outputs.models import Log

    action_type = "CREATE" if created else "UPDATE"
    model_fields = Group._meta.get_fields()
    old = instance.old
    del instance.old
    new = instance

    modification = get_modification(old, new, model_fields, action_type, DROP_FIELD_LOG)
    if modification:
        Log(
            action_type=action_type,
            modified_model_name="Group",
            modified_object_name=instance.name,
            modified_object_id=instance.id,
            modification=modification,
        ).save()


@receiver(post_delete, sender=Group)
def delete_group(sender, instance, using, **kwargs):
    from outputs.models import Log

    action_type = "REMOVE"
    model_fields = Group._meta.get_fields()
    Log(
        action_type=action_type,
        modified_model_name="Group",
        modified_object_name=instance.name,
        modified_object_id=instance.id,
        modification=get_modification(instance, None, model_fields, action_type),
    ).save()


@receiver(pre_save, sender=Group)
def update_or_delete_user_custom_field(sender, instance, using, **kwargs):
    if not instance._state.adding:
        current_device = Group.objects.using(using).get(pk=instance.id)
        update_or_delete_custom_field(current_device, instance)
