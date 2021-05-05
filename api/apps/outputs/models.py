import uuid

from django.db.models import JSONField
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from outputs.middlewares import RequestMiddleware


class Log(models.Model):
    """
    A Log. Contains User's Activity on Platform.
    """

    class Meta:
        ordering = ("id",)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, blank=True, editable=False)
    username = models.CharField(max_length=64, null=True)
    user_id = models.CharField(max_length=64, null=True)
    action_type = models.CharField(max_length=64, null=False)
    modified_model_name = models.CharField(max_length=64, null=False)
    modified_object_name = models.CharField(max_length=64, null=False)
    modified_object_id = models.CharField(max_length=64, null=True)
    modification = JSONField(null=True, blank=True, default=None)
    name = models.CharField(max_length=64, null=True)
    role_name = models.CharField(max_length=64, null=True)
    workspace_name = models.CharField(max_length=64, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.id}>"


@receiver(pre_save, sender=Log)
def add_log(sender, instance, **kwargs):
    request = RequestMiddleware(get_response=None)

    if hasattr(request.thread_local, "current_request"):
        request = request.thread_local.current_request

        if request.user.is_authenticated:
            instance.username = request.user.email
            instance.user_id = request.user.id

        instance.workspace_name = (
            request.workspace_slug if request.workspace_slug is not None else instance.workspace_name
        )

    # Convert UUID into string
    instance.user_id = str(instance.user_id) if instance.user_id is not None else None
    instance.modified_object_id = str(instance.modified_object_id) if instance.modified_object_id is not None else None


def log_group_relation_changes(
    modified_model_name, modified_object_name, modified_object_id, action, pk_set, role_name=None
):

    request = RequestMiddleware(get_response=None)
    username = None
    workspace_name = None
    user_id = None

    if hasattr(request.thread_local, "current_request"):
        request = request.thread_local.current_request
        workspace_name = request.workspace_slug

        if request.user.is_authenticated:
            username = request.user.email
            user_id = request.user.id

    if action == "post_add":
        logs = []
        action_type = "ADD TO GROUP"

        for pk in pk_set:
            # import here to avoid cyclic import with Device
            from groups.models import Group

            group = Group.objects.get(id=pk)
            log = Log(
                username=username,
                user_id=str(user_id),
                action_type=action_type,
                modified_model_name=modified_model_name,
                modified_object_name=modified_object_name,
                modified_object_id=str(modified_object_id),
                name=group.name,
                role_name=role_name,
                workspace_name=workspace_name,
            )
            logs.append(log)
            log = Log(
                username=username,
                user_id=str(user_id),
                action_type=action_type,
                modified_model_name=group.__class__.__name__,
                modified_object_name=group.name,
                modified_object_id=str(group.id),
                name=group.name,
                role_name=role_name,
                workspace_name=workspace_name,
                modification={
                    "new": {"device" if modified_model_name.lower() == "device" else "user": modified_object_name},
                    "old": {},
                },
            )
            logs.append(log)

        if logs:
            Log.objects.bulk_create(logs)
    elif action == "post_remove":
        logs = []
        action_type = "REMOVE FROM GROUP"

        for pk in pk_set:
            # import here to avoid cyclic import with Device
            from groups.models import Group

            group = Group.objects.get(id=pk)
            log = Log(
                username=username,
                user_id=str(user_id),
                action_type=action_type,
                modified_model_name=modified_model_name,
                modified_object_name=modified_object_name,
                modified_object_id=str(modified_object_id),
                name=group.name,
                role_name=role_name,
                workspace_name=workspace_name,
            )
            logs.append(log)
            log = Log(
                username=username,
                user_id=str(user_id),
                action_type=action_type,
                modified_model_name=group.__class__.__name__,
                modified_object_name=group.name,
                modified_object_id=str(group.id),
                name=group.name,
                role_name=role_name,
                workspace_name=workspace_name,
                modification={
                    "new": {},
                    "old": {"device" if modified_model_name.lower() == "device" else "user": modified_object_name},
                },
            )
            logs.append(log)

        if logs:
            Log.objects.bulk_create(logs)
