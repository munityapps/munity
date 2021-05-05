import pytz

from django.utils import timezone
from workspace.models import WorkspaceSettings
from django.conf import settings

class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if WorkspaceSettings.objects.filter(key="time_zone").count() > 0:
            tzname = WorkspaceSettings.objects.get(key="time_zone").value
        else:
            tzname = settings.TIME_ZONE
        timezone.activate(pytz.timezone(tzname))
        return self.get_response(request)