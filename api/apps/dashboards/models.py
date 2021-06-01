import uuid

from django.db.models import JSONField
from django.db import models
from django.db.models.signals import post_delete, post_save, pre_delete, pre_save
from django.dispatch import receiver

from base.operations import get_modification
from graphs.models import Graph
from groups.models import Group
from logs.models import Log
from base.operations import update_or_delete_custom_field

DROP_FIELD_LOG = ["updated_at"]


class Dashboard(models.Model):
    class Meta:
        ordering = ("name",)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    name = models.CharField(max_length=64, unique=True)
    graphs = models.ManyToManyField(Graph, through="DashboardGraphRelationship", related_name="dashboards")
    groups = models.ManyToManyField(Group, through="DashboardGroupRelationship", related_name="dashboards")
    settings = JSONField(default=dict, blank=True, null=True)

    custom_field = JSONField(null=False, blank=True, default=dict)

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.name}>"

    def get_associated_groups(self):
        return [group.pk for group in self.groups.all()]


class DashboardGraphRelationship(models.Model):
    class Meta:
        unique_together = ("dashboard", "graph")

    dashboard_graph_relationship_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    dashboard = models.ForeignKey(Dashboard, on_delete=models.CASCADE, editable=False, related_name="dashboard_graphs")
    graph = models.ForeignKey(Graph, on_delete=models.CASCADE, editable=False, related_name="dashboard_graphs")

    def __repr__(self):
        return f"<{self.__class__.__name__}: ({self.dashboard}, {self.graph})>"


class DashboardGroupRelationship(models.Model):
    class Meta:
        unique_together = ("dashboard", "group")

    dashboard_group_relationship_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dashboard = models.ForeignKey(Dashboard, on_delete=models.CASCADE, editable=False, related_name="dashboard_groups")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, editable=False, related_name="dashboard_groups")

    def __repr__(self):
        return f"<{self.__class__.__name__}: ({self.dashboard}, {self.group})>"


@receiver(post_save, sender=DashboardGraphRelationship)
@receiver(post_delete, sender=DashboardGraphRelationship)
def update_dashabord_groups(sender, instance, using, **kwargs):
    dashboard = instance.dashboard
    DashboardGroupRelationship.objects.filter(dashboard=dashboard).delete()
    for graph in dashboard.graphs.all():
        for group in graph.groups.all():
            if not group in dashboard.groups.all():
                DashboardGroupRelationship.objects.create(dashboard=dashboard, group=group)


# Log Activity
@receiver(pre_save, sender=Dashboard)
@receiver(pre_delete, sender=Dashboard)
def get_old(sender, instance, **kwargs):
    try:
        instance.old = Dashboard.objects.get(pk=instance.pk)
    except Dashboard.DoesNotExist:
        instance.old = None


@receiver(post_save, sender=Dashboard)
def add_dashboard(sender, instance, created, **kwargs):
    action_type = "CREATE" if created else "UPDATE"
    model_fields = Dashboard._meta.get_fields()
    old = instance.old
    del instance.old
    new = instance
    modification = get_modification(old, new, model_fields, action_type, DROP_FIELD_LOG)
    if modification:
        log = Log(
            action_type=action_type,
            modified_model_name="Dashboard",
            modified_object_name=instance.name,
            modified_object_id=instance.dashboard_id,
            modification=modification,
        )
        log.save()


@receiver(post_delete, sender=Dashboard)
def delete_dashboard(sender, instance, using, **kwargs):
    action_type = "REMOVE"
    model_fields = Dashboard._meta.get_fields()
    log = Log(
        action_type=action_type,
        modified_model_name="Dashboard",
        modified_object_name=instance.name,
        modified_object_id=instance.dashboard_id,
        modification=get_modification(instance, None, model_fields, action_type),
    )
    log.save()


@receiver(pre_save, sender=Dashboard)
def update_or_delete_user_custom_field(sender, instance, using, **kwargs):
    if not instance._state.adding:
        current_device = Dashboard.objects.using(using).get(pk=instance.dashboard_id)
        update_or_delete_custom_field(current_device, instance)
