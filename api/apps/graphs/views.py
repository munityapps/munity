import copy
import json

from django.utils.dateparse import parse_duration
from rest_framework import status

from acl.operations import has_workspace_permission
from base.viewsets import MultipleDBModelViewSet, NoCreateMixin, NoDestroyMixin
from dashboards.models import Dashboard, DashboardGraphRelationship
from devices.models import Device
from groups.models import Group
from graphs.models import Graph, PreviewSettings
from graphs.serializers import GraphSerializer, PreviewSettingsSerializer
from rest_framework.response import Response


class GraphViewSet(MultipleDBModelViewSet):
    serializer_class = GraphSerializer
    queryset = Graph.objects.none()

    def get_queryset(self):
        queryset = Graph.objects

        if has_workspace_permission(self.request.user, self.action, self.queryset.model.__name__, self.request):
            # Someone who has workspace permission to GET graphs, can see all graphs
            pass
        else:
            # Else, someone can only see graphs among those that belong to groups they have access to,
            # so we are filtering further: we are only returning the graphs that are in
            # one of the groups the user is in
            user_groups = self.request.user.groups.all()
            queryset = queryset.filter(groups__in=user_groups).distinct()

        return queryset.prefetch_related("dashboards", "devices")

    # @permission_required (not present here because permission checks are applied on self.get_queryset())
    def list(self, request):
        queryset = self.get_queryset()
        if self.request.query_params.get("ids"):
            graphs_id = json.loads(self.request.query_params.get("ids"))
            graphs = queryset.filter(id__in=graphs_id)
            serializer = self.get_serializer(graphs, many=True)
        else:
            serializer = self.get_serializer(queryset, many=True, exclude=("_graph_data",))
        return Response(serializer.data)

        # In the list view, we are excluding the "_graph_data" field
        # serializer = self.get_serializer(queryset, many=True, exclude=("_graph_data",))

        # return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        request_data = copy.deepcopy(request.data)
        dashboard_ids = request_data.pop("dashboard_ids")
        ids = request_data.pop("selected_devices")
        ids = request_data.pop("selected_groups")

        if request_data["start_offset_time"] is not None:
            request_data["start_offset_time"] = parse_duration(request_data.pop("start_offset_time", ""))

        if request_data["start_offset_time"] is None:
            request_data["start_offset_time"] = request_data.pop("start_offset_time", "")

        graph = Graph.objects.create(**request_data)

        for device in ids:
            device_obj = Device.objects.get(pk=device)
            graph.devices.add(device_obj)

        for group in ids:
            group_obj = Group.objects.get(pk=group)
            graph.groups.add(group_obj)

        for dashboard_id in dashboard_ids:
            dashboard = Dashboard.objects.get(pk=dashboard_ids[0])
            _ = DashboardGraphRelationship.objects.create(dashboard=dashboard, graph=graph)

        serializer = self.get_serializer(graph)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PreviewSettingsViewSet(NoCreateMixin, NoDestroyMixin, MultipleDBModelViewSet):
    serializer_class = PreviewSettingsSerializer
    queryset = PreviewSettings.objects.all()

    def get_queryset(self):
        return PreviewSettings.objects.all()

    def list(self, request):

        devices_id = json.loads(self.request.query_params.get("ids"))
        preview_settings = self.queryset.filter(id__in=devices_id)

        serializer = self.get_serializer(preview_settings, many=True)
        return Response(serializer.data)
