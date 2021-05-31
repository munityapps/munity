import pytz

from django.utils import timezone
from settings.models import Settings
from django.conf import settings

class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if Settings.objects.filter(key="time_zone").count() > 0:
            tzname = Settings.objects.get(key="time_zone").value
        else:
            tzname = settings.TIME_ZONE
        timezone.activate(pytz.timezone(tzname))
        return self.get_response(request)

class WorkspaceSlug:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        request.workspace_slug = "munity"
        response = self.get_response(request)
        return response