from rest_framework import viewsets
from django.db.models.query_utils import Q

# Create your views here.
class MunityWorkspaceViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        model = self.serializer_class.Meta.model
        if "workspace_pk" in self.kwargs:
            return model.objects.filter(Q(workspace=None) | Q(workspace=self.kwargs["workspace_pk"]))
        return model.objects.all()
