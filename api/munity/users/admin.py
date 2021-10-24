from django.contrib import admin, auth
from django.contrib.auth.admin import UserAdmin

from .models import User

class MunityUserAdmin(UserAdmin):
    def get_form(self, request, obj=None, change=False, **kwargs):
        kwargs['labels'] = {
            'groups': 'Roles'
        }
        return super().get_form(request, obj=obj, change=change, **kwargs)

admin.site.register(User)

admin.site.unregister(auth.models.Group)