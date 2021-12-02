from django.contrib.contenttypes.models import ContentType
from rest_framework import viewsets
from deepdiff import DeepDiff
from django.db.models.query_utils import Q

from .workspaces.models import Workspace
from .records.models import Record

from .utils import UUIDEncoder

import json

# Create your views here.
class MunityViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        model = self.serializer_class.Meta.model
        if "workspace_pk" in self.kwargs:
            return model.objects.filter(Q(workspace=None) | Q(workspace=self.kwargs["workspace_pk"]))
        return model.objects.all()

    def destroy(self, request, workspace_pk=None, pk=None):
        deleted_model = self.serializer_class.Meta.model.objects.get(pk=pk)
        ctype = ContentType.objects.get_for_model(deleted_model)
        response = super().destroy(request, workspace_pk, pk=pk)
        record = Record.objects.create(
            previous_value = None,
            diff_value = None,
            action = 'delete',
            workspace = Workspace.objects.get(slug=workspace_pk),
            user = request.user,
            product_object_id = pk,
            product_content_type = ctype
        )
        record.save()
        return response

    def create(self, request, workspace_pk=None):
        response = super().create(request, workspace_pk)
        model_id = dict(response.data).get('id')
        new_model = self.serializer_class.Meta.model.objects.get(pk=model_id)
        ctype = ContentType.objects.get_for_model(new_model)
        record = Record.objects.create(
            previous_value = None,
            diff_value = None,
            action = 'create',
            workspace = Workspace.objects.get(slug=workspace_pk),
            user = request.user,
            product_object_id = model_id,
            product_content_type = ctype
        )
        record.save()
        return response

    def update(self, request, workspace_pk=None, pk=None, partial=False):
        old_model = self.serializer_class.Meta.model.objects.get(pk=pk)
        response = super().update(request, workspace_pk, pk)
        new_model = self.serializer_class.Meta.model.objects.get(pk=pk)
        diff = DeepDiff(
            old_model,
            new_model,
            exclude_paths=["root.modified"]
        )
        ctype = ContentType.objects.get_for_model(old_model)
        if diff:
            record = Record.objects.create(
                previous_value = json.dumps(self.serializer_class(old_model).data, cls=UUIDEncoder),
                diff_value = diff,
                action = 'update',
                workspace = Workspace.objects.get(slug=workspace_pk),
                user = request.user,
                product_object_id = pk,
                product_content_type = ctype
            )
            record.save()
        return response

