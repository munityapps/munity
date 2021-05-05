from django.conf import settings
from django.core.paginator import EmptyPage, Paginator

from acl.operations import has_workspace_permission, permission_required
from base.viewsets import MultipleDBModelViewSet
from dashboards.models import Dashboard
from dashboards.serializers import DashboardSerializer
from rest_framework.response import Response


class DashboardViewSet(MultipleDBModelViewSet):
    serializer_class = DashboardSerializer
    queryset = Dashboard.objects.none()

    def get_queryset(self):
        queryset = Dashboard.objects

        if has_workspace_permission(self.request.user, self.action, self.queryset.model.__name__, self.request):
            # Someone who has workspace permission to GET dashboards, can see all dashboards
            pass
        else:
            # Else, someone can only see dashboards among those that belong to groups they have access to,
            # so we are filtering further: we are only returning the dashboards that are in
            # one of the groups the user is in
            user_groups = self.request.user.groups.all()
            queryset = queryset.filter(groups__in=user_groups).distinct()

        return queryset

    # @permission_required (not present here because permission checks are applied on self.get_queryset())
    def list(self, request, page=None, step=None):
        queryset = self.get_queryset()
        # for list of Dasboards, we don't want "dashboards-graphs"
        serializer = self.get_serializer(queryset, many=True)

        if step == None:
            step = settings.PAGE_SIZE
        count = len(serializer.data)
        if page is not None:
            # Pagination
            paginator = Paginator(serializer.data, step)
            try:
                return Response(data={"count": count, "results": list(paginator.get_page(page))})
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                return Response(data=[])

        return Response(serializer.data)

    @permission_required
    def bulk_destroy(self, request, *args, pk=None, **kwargs):
        dashboard_ids = request.data.get("dashboard_ids")
        dashboards = Dashboard.objects.filter(pk__in=dashboard_ids)

        nb_dashboards_deleted = len(dashboards)
        self.perform_bulk_destroy(dashboards)

        return Response(data={"nb_dashboards_deleted": nb_dashboards_deleted})
