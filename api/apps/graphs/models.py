import uuid

from django.contrib.postgres.fields import ArrayField
from django.db.models import JSONField
from django.db import models
from django.db.models.signals import post_delete, post_save, pre_delete, pre_save
from django.dispatch import receiver
from django.utils import timezone

from base.operations import get_modification, update_or_delete_custom_field
from data_connector import data_connector
from devices.models import Device
from groups.models import Group
from logs.models import Log
from rest_framework.exceptions import ValidationError

class GraphConditionalFormatting(models.Model):
    """
    (Optional) Describes the Conditional Formatting parameters for a Graph.
    """

    normal_color = ArrayField(base_field=models.CharField(max_length=64), default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    alert_color = models.CharField(max_length=64)
    alert_color_threshold_value = models.FloatField()


class Graph(models.Model):
    class Meta:
        ordering = ("name",)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    name = models.CharField(max_length=64)
    type = models.CharField(max_length=64)
    is_last_value = models.BooleanField()  # True: "last_value"; False: "history"
    # is_seuil = models.BooleanField(default=False)
    device_data_types = ArrayField(base_field=models.CharField(max_length=64))
    # device_data_min_max = JSONField(default=dict, blank=True, null=True)

    from_timestamp = models.DateTimeField(default=None, null=True, blank=True)
    to_timestamp = models.DateTimeField(default=None, null=True, blank=True)
    start_offset_time = models.DurationField(default=None, null=True, blank=True)

    aggregate_period_name = models.CharField(null=True, blank=True, max_length=32)
    aggregate_operation_name = models.CharField(
        max_length=64, default=None, null=True, blank=True
    )

    devices = models.ManyToManyField(Device, related_name="graphs")
    groups = models.ManyToManyField(Group, related_name="graphs")

    custom_field = JSONField(null=False, blank=True, default=dict)

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.name}>"

    def save(self, *args, **kwargs):
        if self.aggregate_period_name is not None:
            if self.aggregate_operation_name is None:
                raise ValidationError(
                    "You must specify 'aggregate_operation_name' since you specified 'aggregate_period_name'."
                )
        if not self.is_last_value:
            if self.start_offset_time and (self.from_timestamp or self.to_timestamp):
                raise ValidationError(
                    f"You can only specify either start_offset_time or (from_timestamp and to_timestamp)"
                )
            elif not self.start_offset_time and (not self.from_timestamp or not self.to_timestamp):
                raise ValidationError(f"You must specify either start_offset_time or (from_timestamp and to_timestamp)")

        super().save(*args, **kwargs)

    def get_associated_groups(self):
        """This function is required for ACL's. It returns the list of groups this graph belongs to."""
        return [self.groups]

    def get_associated_devices(self):
        """This function returns all devices associated with this Graph"""
        devices = []
        for group in self.groups.all():
            devices_related = group.get_related_devices()
            for device in devices_related:
                if device not in devices:
                    devices.append(device)
        for device in self.devices.all():
            if not device in devices:
                devices.append(device)
        return devices

    def get_graph_data(self):
        """
            Query the Startup API for graph data.
            Generate graph_from_ts and graph_to_ts with the current time and the periode
        """
        devices = self.get_associated_devices()

        try:
            if self.start_offset_time:
                from_timestamp = timezone.now() - self.start_offset_time
                to_timestamp = timezone.now()
            else:
                from_timestamp = self.from_timestamp
                to_timestamp = self.to_timestamp

            graph_data = data_connector.get_device_data(
                devices=[device.reference for device in devices],
                data_types=self.device_data_types,
                is_last_value=self.is_last_value,
                from_timestamp=from_timestamp,
                to_timestamp=to_timestamp,
                aggregate_period_name=self.aggregate_period_name,
                aggregate_operation_name=self.aggregate_operation_name,
                # decimal_places=self.decimal_places,
            )
        except Exception as e:
            print(e)
            graph_data = []
        return graph_data


class PreviewSettings(models.Model):
    device = models.OneToOneField(Device, on_delete=models.CASCADE, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    graph_type = models.CharField(max_length=64, default="table")
    device_data_types = ArrayField(base_field=models.CharField(max_length=64), default=list, blank=True)
    from_timestamp = models.DateTimeField(default=None, null=True, blank=True)
    to_timestamp = models.DateTimeField(default=None, null=True, blank=True)
    start_offset_time = models.DurationField(default=None, null=True, blank=True)
    aggregate_period_name = models.CharField(null=True, blank=True, max_length=32)
    aggregate_operation_name = models.CharField(
        max_length=64, default=None, null=True, blank=True
    )
    custom_field = JSONField(null=False, blank=True, default=dict)

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.device.reference}>"

# Log Activity
@receiver(pre_save, sender=Graph)
@receiver(pre_delete, sender=Graph)
def get_old(sender, instance, **kwargs):
    try:
        instance.old = Graph.objects.get(pk=instance.pk)
    except Graph.DoesNotExist:
        instance.old = None


@receiver(post_save, sender=Graph)
def add_graph(sender, instance, created, **kwargs):
    action_type = "CREATE" if created else "UPDATE"
    model_fields = Graph._meta.get_fields()
    old = instance.old
    del instance.old
    new = instance
    log = Log(
        action_type=action_type,
        modified_model_name="Graph",
        modified_object_name=instance.name,
        modified_object_id=instance.id,
        name=None,
        modification=get_modification(old, new, model_fields, action_type),
    ).save()


@receiver(post_delete, sender=Graph)
def delete_graph(sender, instance, using, **kwargs):
    action_type = "REMOVE"
    model_fields = Graph._meta.get_fields()
    log = Log(
        action_type=action_type,
        modified_model_name="Graph",
        modified_object_name=instance.name,
        modified_object_id=instance.id,
        name=None,
        modification=get_modification(instance, None, model_fields, action_type),
    ).save()


@receiver(pre_save, sender=Graph)
def update_or_delete_user_custom_field(sender, instance, using, **kwargs):
    if not instance._state.adding:
        current_device = Graph.objects.using(using).get(pk=instance.id)
        update_or_delete_custom_field(current_device, instance)
