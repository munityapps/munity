# from rest_framework_extensions.routers import ExtendedDefaultRouter as DefaultRouter
from rest_framework_nested import routers as nested_routers

from .authorization.views import PermissionsViewSet, RolesViewSet
from .users.views import UsersViewSet
from .generic_groups.views import GenericGroupsViewSet
from .workspaces.views import WorkspacesViewSet
from .settings.views import SettingsViewSet
from .files.views import FileViewSet

overmind_router = nested_routers.SimpleRouter()
overmind_router.register(r"users", UsersViewSet, basename="user")
overmind_router.register(r"workspaces", WorkspacesViewSet, basename="workspace")
overmind_router.register(r"roles", RolesViewSet, basename="role")
overmind_router.register(r"generic_groups", GenericGroupsViewSet, basename="group")
overmind_router.register(r"permissions", PermissionsViewSet, basename="permission")
overmind_router.register(r"settings", SettingsViewSet, basename="settings")
overmind_router.register(r"files", FileViewSet, basename="files")

workspace_router = nested_routers.NestedSimpleRouter(overmind_router, r'workspaces', lookup='workspace')
workspace_router.register(r"users", UsersViewSet, basename="workspace-user")
workspace_router.register(r"roles", RolesViewSet, basename="workspace-user")
workspace_router.register(r"generic_groups", GenericGroupsViewSet, basename="workspace-user")
workspace_router.register(r"permissions", PermissionsViewSet, basename="workspace-user")
workspace_router.register(r"settings", SettingsViewSet, basename="setting")
workspace_router.register(r"files", FileViewSet, basename="files")
