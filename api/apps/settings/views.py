import ast

from django.db.models import query

from base.viewsets import NoDestroyMixin
from rest_framework import status
from rest_framework.response import Response
from base.viewsets import MultipleDBModelViewSet
from .models import Settings
from .serializers import SettingsSerializer

def get_literal_eval(value):
    try:
        value = ast.literal_eval(value)
    except:
        pass
    return value

class SettingsViewSet(MultipleDBModelViewSet):
    serializer_class = SettingsSerializer
    queryset = Settings.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            key = list(request.data.keys())[0]
            settings = Settings.objects.create(key=key, value=str(request.data.get(key)))
        except Exception as e:
            raise e

        if settings:
            serializer = self.get_serializer(settings)
            value = get_literal_eval(serializer.data.get("value"))

            return Response({serializer.data.get("key"): value}, status=status.HTTP_201_CREATED)

        return Response({}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        queryset = self.get_queryset()
        default_settings = {}
        default_settings['toast_success_color'] = '#24AB68'
        default_settings['toast_error_color'] = '#ED7474'
        default_settings['max_displayable_users'] = '3'

        for row in queryset:
            value = get_literal_eval(row.value)
            default_settings[row.key] = value
        return Response(default_settings)

    def update(self, request, pk=None):
        key = list(request.data.keys())[0]
        settings, created = Settings.objects.get_or_create(key=key)

        data = {"value": str(request.data.get(key))}
        serializer = self.get_serializer(settings, data=data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

        value = get_literal_eval(serializer.data.get("value"))

        return Response({serializer.data.get("key"): value})

    def partial_update(self, request, pk=None):
        return self.update(request, pk=pk)

    def partial_bulk_update(self, request, pk=None):
        return self.update(request, pk=pk)