from enum import Enum

from accounts.models import User, UserGroupMembership
from acl.models import (
    GroupACL,
    GroupAction,
    GroupResource,
    GroupRole,
    WorkspaceACL,
    WorkspaceAction,
    WorkspaceResource,
    WorkspaceRole,
)
from dashboards.models import Dashboard, DashboardGraphRelationship
from devices.models import Device
from graphs.models import Graph, PreviewSettings
from groups.models import Group
from invites.models import Invite, InviteGroupMembership
from settings.models import Settings
from outputs.models import Log

class DefaultWorkspaceRoleChoice(Enum):
    """Enum for workspace Roles
    Careful: These Workspace Roles are written in order of power.
    This has its importance because a User cannot give another User a higher-ranked role than his own.
    """

    OWNER = "Owner"
    ADMIN = "Admin"
    USER = "User"


class DefaultGroupRoleChoice(Enum):
    """Enum for group Roles"""

    ADMIN = "Admin"
    USER = "User"


class DefaultWorkspaceActionChoice(Enum):
    """Enum for ACL Actions"""

    READ = "READ"
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    ADD_TO_GROUP = "ADD_TO_GROUP"
    REMOVE_FROM_GROUP = "REMOVE_FROM_GROUP"


class DefaultGroupActionChoice(Enum):
    """Enum for ACL Actions"""

    READ = "READ"
    UPDATE = "UPDATE"
    ADD_TO_GROUP = "ADD_TO_GROUP"
    REMOVE_FROM_GROUP = "REMOVE_FROM_GROUP"


DRF_ACTION_MAP = {
    # This maps Django REST Framework's default action names to classical CRUD action names.
    "list": DefaultWorkspaceActionChoice.READ.value,
    "retrieve": DefaultWorkspaceActionChoice.READ.value,
    "create": DefaultWorkspaceActionChoice.CREATE.value,
    "bulk_create": DefaultWorkspaceActionChoice.CREATE.value,
    "update": DefaultWorkspaceActionChoice.UPDATE.value,
    "bulk_update": DefaultWorkspaceActionChoice.UPDATE.value,
    "partial_update": DefaultWorkspaceActionChoice.UPDATE.value,
    "partial_bulk_update": DefaultWorkspaceActionChoice.UPDATE.value,
    "destroy": DefaultWorkspaceActionChoice.DELETE.value,
    "bulk_destroy": DefaultWorkspaceActionChoice.DELETE.value,
    "get_or_create": DefaultWorkspaceActionChoice.READ.value,
    "update_or_create": DefaultWorkspaceActionChoice.UPDATE.value,
}

ALL_WORKSPACE_RESOURCES = [
    # Resources Workspace Owners and Admins have every right to.
    # If you change anything here, you will need to run `python manage.py init_db`
    Settings,
    WorkspaceRole,
    WorkspaceAction,
    WorkspaceResource,
    WorkspaceACL,
    GroupRole,
    GroupAction,
    GroupResource,
    GroupACL,
    User,
    Group,
    UserGroupMembership,
    Device,
    Dashboard,
    DashboardGraphRelationship,
    Graph,
    PreviewSettings,
    Invite,
    InviteGroupMembership,
    Log,
]

ALL_GROUP_RESOURCES = [
    # Resources that are submitted to the Group ACL's
    # If you change anything here, you will need to run `python manage.py init_db`
    Group,
    Device,
    Dashboard,
    Graph,
    UserGroupMembership,
    InviteGroupMembership,
]

USER_WORKSPACE_RESOURCES = [
    # Resources Workspace Users have READ access to
    # If you change anything here, you will need to run `python manage.py init_db`
    WorkspaceRole,
    WorkspaceAction,
    WorkspaceResource,
    WorkspaceACL,
    GroupRole,
    GroupAction,
    GroupResource,
    GroupACL,
    User,
    PreviewSettings,
]

READ_AND_UPDATE_WORKSPACE_RESOURCES = [
    # Resources Everybody has READ and UPDATE rights to. (No CREATE/DELETE or ADD_TO_GROUP/REMOVE_FROM_GROUP)
    # If you change anything here, you will need to run `python manage.py init_db`
]

assert set(ALL_GROUP_RESOURCES).isdisjoint(
    set(USER_WORKSPACE_RESOURCES)
), "No resource should be both in ALL_GROUP_RESOURCES and USER_WORKSPACE_RESOURCES"

assert set(ALL_GROUP_RESOURCES + USER_WORKSPACE_RESOURCES).issubset(
    set(ALL_WORKSPACE_RESOURCES)
), "You probably forgot to put a model in ALL_WORKSPACE_RESOURCES"

for group_resource_class in ALL_GROUP_RESOURCES:
    assert hasattr(
        group_resource_class, "get_associated_groups"
    ), f"As a GROUP_RESOURCE, class '{group_resource_class.__name__}' should implement a 'get_associated_groups()' method for the acl operations to work. This method should return a _list_ or _queryset_ containing all groups the resource is affiliated to. See the models of other Group Resources for examples."
