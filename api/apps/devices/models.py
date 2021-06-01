import uuid

from django.db.models import JSONField
from django.db import models
from django.db.models.signals import m2m_changed, post_delete, post_save, pre_delete, pre_save
from django.dispatch import receiver

from base.operations import get_modification
from data_connector import data_connector
from django_bulk_update.manager import BulkUpdateManager
from groups.models import Group
from logs.models import Log, log_group_relation_changes
from base.operations import update_or_delete_custom_field

DROP_FIELD_LOG = ["updated_at"]


class Device(models.Model):
    class Meta:
        ordering = ("name",)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    reference = models.CharField(db_index=True, blank=True, max_length=128, unique=True)
    name = models.CharField(default="", blank=True, max_length=64)
    address = models.CharField(default="", blank=True, max_length=128)
    position = models.CharField(default="", blank=True, max_length=64)
    description = models.CharField(default="", blank=True, max_length=256)
    groups = models.ManyToManyField(Group, related_name="devices")
    last_triggered_timestamps = JSONField(null=True, blank=True, default=None)

    custom_field = JSONField(null=False, blank=True, default=dict)

    objects = BulkUpdateManager()
    # graphs (reverse ManyToManyField(Graph))

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.reference}>"

    def __str__(self):
        return f"{self.name} ({self.reference})"

    def get_associated_groups(self):
        """This function is required for ACL's. It returns the list of groups this device belongs to."""
        return self.groups.all()

    def get_device_data(self, *args, **kwargs):
        """Query the Startup API for device data."""
        try:
            device_data = data_connector.get_device_data(
                devices={self.reference: self.name}, is_last_value=True, *args, **kwargs
            )
        except Exception as e:
            print(e)
            device_data = []
        return device_data


# Signal send after a save() method is called by a Device instance.
# dispatch_uid is a unique identifier, permitting to avoid this bug:
# https://code.djangoproject.com/wiki/Signals#TipsandTroubleshooting
@receiver(post_save, sender=Device, dispatch_uid="apps.devices.models.py")
def save_related_preview_settings(sender, instance, created, using, **kwargs):
    """When a Device object is created, a PreviewSettings object is also created and associated to it."""
    # import here to avoid cyclic import with Device
    from graphs.models import PreviewSettings

    if created:
        PreviewSettings.objects.using(using).create(device=instance)


def bulk_save_related_preview_settings(devices_to_create, using):
    # post_save() signal function doesn't happen after bulk_create()
    # So use this function to create Device PreviewSettings when `bulk_create()` is called

    # Import here to avoid cyclic import with Device
    from graphs.models import PreviewSettings

    previewsettings_to_create = []
    for device in devices_to_create:
        new_preview = PreviewSettings(device=device)
        previewsettings_to_create.append(new_preview)

    PreviewSettings.objects.using(using).bulk_create(previewsettings_to_create)


# Log Activity
@receiver(pre_save, sender=Device)
@receiver(pre_delete, sender=Device)
def get_old(sender, instance, **kwargs):
    try:
        instance.old = Device.objects.get(pk=instance.pk)
    except Device.DoesNotExist:
        instance.old = None


@receiver(post_save, sender=Device)
def add_device(sender, instance, created, **kwargs):
    action_type = "CREATE" if created else "UPDATE"
    model_fields = Device._meta.get_fields()
    old = instance.old
    del instance.old
    new = instance

    # To prevent save meaningless Log when `ADD TO GROUP` or `REMOVE FROM GROUP`
    modification = get_modification(old, new, model_fields, action_type, DROP_FIELD_LOG)

    if modification:
        log = Log(
            action_type=action_type,
            modified_model_name="Device",
            modified_object_name=instance.reference,
            modified_object_id=instance.id,
            modification=modification,
        ).save()


@receiver(post_delete, sender=Device)
def delete_device(sender, instance, using, **kwargs):
    action_type = "REMOVE"
    model_fields = Device._meta.get_fields()
    log = Log(
        action_type=action_type,
        modified_model_name="Device",
        modified_object_name=instance.reference,
        modified_object_id=instance.id,
        modification=get_modification(instance, None, model_fields, action_type),
    ).save()


@receiver(m2m_changed, sender=Device.groups.through)
def update_device_group_relations(sender, **kwargs):
    instance = kwargs.pop("instance", None)
    pk_set = kwargs.pop("pk_set", None)
    action = kwargs.pop("action", None)

    log_group_relation_changes("Device", instance.reference, instance.id, action, pk_set)


@receiver(pre_save, sender=Device)
def update_or_delete_device_custom_field(sender, instance, using, **kwargs):
    if not instance._state.adding:
        current_device = Device.objects.using(using).get(pk=instance.id)
        update_or_delete_custom_field(current_device, instance)


def log_bulk_change(devices, action_type, old_devices_to_save=None):
    model_fields = Device._meta.get_fields()

    if action_type == "CREATE":
        for device in devices:
            log = Log(
                action_type=action_type,
                modified_model_name="Device",
                modified_object_name=device.reference,
                modified_object_id=device.id,
                modification=get_modification(None, device, model_fields, action_type),
            ).save()
    elif action_type == "UPDATE":
        for index, device in enumerate(devices):
            log = Log(
                action_type=action_type,
                modified_model_name="Device",
                modified_object_name=device.reference,
                modified_object_id=device.id,
                modification=get_modification(old_devices_to_save[index], device, model_fields, action_type),
            ).save()
