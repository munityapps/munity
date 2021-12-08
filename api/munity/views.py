from django.contrib.contenttypes.models import ContentType
from rest_framework import viewsets
from deepdiff import DeepDiff

from .workspaces.models import Workspace
from .records.models import Record

from .utils import UUIDEncoder

import json

# Create your views here.
class MunityViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        model = self.serializer_class.Meta.model

        # filter request to current model workspace
        if "workspace_pk" in self.kwargs:
            return model.objects.filter(workspace=self.kwargs["workspace_pk"])
        return model.objects.all()

    def destroy(self, request, pk=None, workspace_pk=None):
        # store model that will be deleted
        deleted_model = self.serializer_class.Meta.model.objects.get(pk=pk)

        # get its content type
        ctype = ContentType.objects.get_for_model(deleted_model)

        # destroy item
        response = super().destroy(request=request, workspace_pk=workspace_pk, pk=pk)

        # record the vicious action!
        record = Record.objects.create(
            previous_value = None,
            diff_value = None,
            action = 'delete',
            workspace = Workspace.objects.filter(slug=workspace_pk).first(),
            user = request.user,
            product_object_id = pk,
            product_content_type = ctype
        )
        record.save()
        return response

    def create(self, request, workspace_pk=None):
        # getting workspace
        current_workspace = Workspace.objects.filter(slug=workspace_pk).first()

        # add new workspace params
        request.data['workspace'] = current_workspace

        # get response
        response = super().create(request=request, workspace_pk=workspace_pk)

        # storing record
        model_id = dict(response.data).get('id')
        new_model = self.serializer_class.Meta.model.objects.get(pk=model_id)
        ctype = ContentType.objects.get_for_model(new_model)
        record = Record.objects.create(
            previous_value = None,
            diff_value = None,
            action = 'create',
            workspace = current_workspace,
            user = request.user,
            product_object_id = model_id,
            product_content_type = ctype
        )
        record.save()
        return response

    def update(self, request, pk=None, workspace_pk=None, partial=False):
        # for now we API cannot move item across workspace, we dont add workspace to serializer

        # keep a record for old data
        old_model = self.serializer_class.Meta.model.objects.get(pk=pk)

        # update model
        response = super().update(request, pk=pk, workspace_pk=workspace_pk, partial=partial)

        # get new data
        new_model = self.serializer_class.Meta.model.objects.get(pk=pk)

        # calculate diff
        diff = DeepDiff(
            old_model,
            new_model,
            exclude_paths=["root.modified"]
        )
        ctype = ContentType.objects.get_for_model(old_model)

        # store record if change was made
        if diff:
            record = Record.objects.create(
                previous_value = json.dumps(self.serializer_class(old_model).data, cls=UUIDEncoder),
                diff_value = diff.get("values_changed"),
                action = 'update',
                workspace = Workspace.objects.filter(slug=workspace_pk).first(),
                user = request.user,
                product_object_id = pk,
                product_content_type = ctype
            )
            record.save()
        return response

