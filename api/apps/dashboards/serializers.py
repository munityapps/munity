from rest_framework import serializers

from acl.operations import has_workspace_permission
from base.serializers import ModelSerializerWithFields
from dashboards.models import Dashboard, DashboardGraphRelationship, DashboardGroupRelationship


class DashboardGraphRelationshipSerializer(ModelSerializerWithFields):
    class Meta:
        model = DashboardGraphRelationship
        exclude = ("graph",)

    id = serializers.UUIDField()
    ids = serializers.SerializerMethodField(read_only=True)

    def get_ids(self, dashboardGraphRelationship):
        groups = dashboardGraphRelationship.graph.groups.all()
        return [group.pk for group in groups]


class DashboardGroupRelationshipSerializer(ModelSerializerWithFields):
    class Meta:
        model = DashboardGroupRelationship
        exclude = ("graph",)

    id = serializers.UUIDField()


class DashboardSerializer(ModelSerializerWithFields):
    class Meta:
        model = Dashboard
        fields = "__all__"

    graphs = serializers.SerializerMethodField(read_only=True)
    ids = serializers.SerializerMethodField(read_only=True)

    def get_graphs(self, dashboard):
        queryset = dashboard.dashboard_graphs

        if not has_workspace_permission(
            self.context["request"].user, self.context["view"].action, self.__class__.Meta.model.__name__, self.context['request']
        ):
            queryset = queryset.filter(graph__groups__in=self.context["request"].user.groups.all())
        else:
            queryset = queryset.all()

        return DashboardGraphRelationshipSerializer(queryset, many=True, read_only=True, exclude=("dashboard",)).data

    def get_ids(self, dashboard):
        queryset = dashboard.dashboard_groups

        if not has_workspace_permission(
            self.context["request"].user, self.context["view"].action, self.__class__.Meta.model.__name__, self.context['request']
        ):
            queryset = queryset.filter(group__in=self.context["request"].user.groups.all())

        ids = list(set(queryset.values_list("group__id", flat=True)))
        return ids
