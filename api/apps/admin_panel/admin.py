from django.contrib import admin
from django.contrib.sites.models import Site
from django.contrib.auth.models import Group as DjangoGroup
# from social_django.models import Association, Nonce, UserSocialAuth
from settings.models import Settings
#
## Generic configuration
admin.site.site_header = "Munity Admin Dashboard"
admin.site.site_title = "Munity Admin Portal"
admin.site.index_title = "Welcome to Munity Researcher Portal"
#try:
#    logo_no_text_url = WorkspaceSettings.objects.get(key="logo_no_text_url").value
#except:
#    pass
#
admin.site.unregister(Site)
# admin.site.unregister(Association)
admin.site.unregister(DjangoGroup)
# admin.site.unregister(Nonce)
# admin.site.unregister(UserSocialAuth)
#