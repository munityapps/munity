from rest_framework import serializers, viewsets
from munity.generic_groups.models import GenericGroup
from django.db.models.query_utils import Q

from munity.workspaces.models import Workspace

# Create your views here.
class MunityWorkspaceViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        model = self.serializer_class.Meta.model
        if "workspace_pk" in self.kwargs:
            return model.objects.filter(Q(workspace=self.kwargs["workspace_pk"]))
        return model.objects.all()
