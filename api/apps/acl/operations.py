"""
Helper functions that check permissions on the ACL.
"""

from inspect import signature

from django.conf import settings

from users.models import UserGroupMembership
from acl.models import GroupACL, WorkspaceACL
from groups.models import Group
from munity.settings_acl import (
    ALL_GROUP_RESOURCES,
    DRF_ACTION_MAP,
    DefaultGroupActionChoice,
    DefaultWorkspaceActionChoice,
)
from rest_framework.exceptions import NotAuthenticated, PermissionDenied

GROUP_ACTIONS = tuple(
    drf_action
    for drf_action, rest_action in DRF_ACTION_MAP.items()
    if rest_action in [a.value for a in DefaultGroupActionChoice]
)


def has_workspace_permission(user, action, resource, request=None):
    """
    Returns True if 'user' has a workspace-level role that allows them to do 'action' on 'resource'.
    Returns False otherwise.
    """

    # master api key has all rights
    if request and hasattr(request, 'is_master_api_key') and request.is_master_api_key:
        return True

    if user and hasattr(user, 'workspace_role_id'):
        return WorkspaceACL.objects.filter(
            workspace_role_id=user.workspace_role_id,
            workspace_action__workspace_action_name=DRF_ACTION_MAP.get(action, action),
            workspace_resource__workspace_resource_name=resource,
        ).exists()

    return False


def _has_group_permission_on_resource_object(
    user, action, resource_object=None, resource_name=None, resource_group_objects=None
):
    """
    Returns True if 'user' has a role inside 'group' that allows them to do 'action' on 'resource'.
    Returns False otherwise.

    A user has group_permission if he has a 'role' in any of the resource's 'resource_group_objects', that can do
    'action' on 'resource'.
    """

    # You can choose to pass this function either ('resource_object') or ('resource_name' and 'group')
    if (resource_object is not None) and (resource_name is resource_group_objects is None):
        resource_group_objects = resource_object.get_associated_groups()
        resource_name = resource_object.__class__.__name__
    elif (resource_object is None) and (resource_name is not None and resource_group_objects is not None):
        assert isinstance(resource_name, str), "Argument 'resource_name' must be of type str."
        assert isinstance(resource_group_objects, list), "Argument 'resource_group_objects' must be of type list."
    else:
        raise AttributeError("You_must_specify_either_('resource_object')_or_('resource_name'_and_'group')")

    try:
        # Get the user's GroupRoles for the resource's Group
        group_role_ids = (
            UserGroupMembership.objects.filter(user=user, group__in=resource_group_objects)
            .only("group_role_id")
            .values_list("group_role_id", flat=True)
        )
    except UserGroupMembership.DoesNotExist:
        return False

    # Check for GroupACL's: If any of the user's GroupRoles can do action on resource, return True
    return GroupACL.objects.filter(
        group_role_id__in=group_role_ids,
        group_action__group_action_name=DRF_ACTION_MAP[action],
        group_resource__group_resource_name=resource_name,
    ).exists()


def check_group_diff_permission(user, resource_name, ids_before, ids_after):
    """
    Check ADD_TO_GROUP and REMOVE_FROM_GROUP permissions based on the diff between ids_before and ids_after.
    """

    assert isinstance(ids_before, list), f"ids_before should be a list. Got type {type(ids_before)}."
    assert isinstance(ids_after, list), f"ids_after should be a list. Got type {type(ids_after)}."

    add_to_groups = list(set(ids_after) - set(ids_before))
    remove_from_groups = list(set(ids_before) - set(ids_after))

    # WORKSPACE ACLs CHECK -----------------------------------------------------------------------------------------
    has_workspace_add_to_group_perm = WorkspaceACL.objects.filter(
        workspace_role_id=user.workspace_role_id,
        workspace_action__workspace_action_name=DefaultWorkspaceActionChoice.ADD_TO_GROUP.value,
        workspace_resource__workspace_resource_name=resource_name,
    ).exists()
    has_workspace_remove_from_group_perm = WorkspaceACL.objects.filter(
        workspace_role_id=user.workspace_role_id,
        workspace_action__workspace_action_name=DefaultWorkspaceActionChoice.REMOVE_FROM_GROUP.value,
        workspace_resource__workspace_resource_name=resource_name,
    ).exists()

    # GROUP ACLs CHECK if the user does not have the necessary Workspace ACLs --------------------------------------
    if (add_to_groups and not has_workspace_add_to_group_perm) or (
        remove_from_groups and not has_workspace_remove_from_group_perm
    ):
        # Get all group_role_ids for all groups the user wants to add or remove
        group_role_ids = []
        for id in add_to_groups * (not has_workspace_add_to_group_perm) + remove_from_groups * (
            not has_workspace_remove_from_group_perm
        ):
            group_role_id = (
                UserGroupMembership.objects.filter(user=user, id=id)
                .only("group_role_id")
                .values_list("group_role_id", flat=True)
            )
            if group_role_id:
                group_role_ids.append(group_role_id[0])
            else:
                # If there is any Group for which the user does not have a UserGroupMembership
                return False

        # Check whether for each group the user wants to add or remove, there is a group_acl that allows him to do so
        # given their group_role_id inside each group
        group_acl_count = (
            GroupACL.objects.none()
            .union(
                *(
                    GroupACL.objects.filter(
                        group_role_id=group_role_id,
                        group_action__group_action_name=group_action_name,
                        group_resource__group_resource_name=resource_name,
                    )[:1]
                    for group_role_id, group_action_name in zip(
                        group_role_ids,
                        [
                            DefaultGroupActionChoice.ADD_TO_GROUP.value
                            for _ in add_to_groups
                            if not has_workspace_add_to_group_perm
                        ]
                        + [
                            DefaultGroupActionChoice.REMOVE_FROM_GROUP.value
                            for _ in remove_from_groups
                            if not has_workspace_remove_from_group_perm
                        ],
                    )
                ),
                all=True,
            )
            .count()
        )
        has_all_remaining_group_acl_perms = group_acl_count == len(
            add_to_groups * (not has_workspace_add_to_group_perm)
            + remove_from_groups * (not has_workspace_remove_from_group_perm)
        )
        return has_all_remaining_group_acl_perms

    else:
        # If the user has the necessary WorkspaceACLs, that is all we need to check
        return True


def user_has_permission(request, user, action, pk=None, resource_model=None):
    """
    General function that checks whether the user has permission to do action on resource,
    according to WorkspaceACLs, GroupACLs, and Group Diff.
    """
    assert user is not None, "user cannot be None"
    resource_name = resource_model.__name__

    # Perform a regular check whether the user can do action on resource
    has_perm = has_workspace_permission(user, action, resource_name, request)
    if not has_perm and pk is not None:
        # A User can always modify their profile, with the exception of certain attributes such as workspace_role_id.
        if str(user.pk) == pk:
            has_perm = True

        elif resource_model in ALL_GROUP_RESOURCES and action in GROUP_ACTIONS:
            resource_object = resource_model.objects.get(pk=pk)
            has_perm = has_perm or _has_group_permission_on_resource_object(user, action, resource_object)

    # If the user is trying to modify which groups are associated with the resource in question, perform an additional
    if (
        hasattr(request, "data")
        and (
            # By convention, if you associate groups to a resource, it must be through an attribute matching "id(s)?"
            any(attribute in request.data for attribute in ("id", "ids"))
            or DRF_ACTION_MAP[action] == "DELETE"
        )
        and resource_model in ALL_GROUP_RESOURCES
        and resource_model is not Group
        and action in DRF_ACTION_MAP.keys()
    ):
        if "id" in request.data:
            new_ids_for_resource = [request.data.get("id")]
        else:
            new_ids_for_resource = request.data.get("ids", [])
        assert isinstance(new_ids_for_resource, list)

        try:
            try:
                resource_object
            except:
                assert (
                    pk is not None
                ), f"Error: Tried to perform {action} on an object that does not exist (pk is None)."
                resource_object = resource_model.objects.get(pk=pk)
            finally:
                resource_initial_ids = [group.pk for group in resource_object.get_associated_groups()]
        except:
            # In case of a CREATE, we cannot fetch the initial groups of a resource that does not already exist,
            # but we know it is an empty list
            resource_initial_ids = []

        has_group_diff_perm = check_group_diff_permission(
            user, resource_name, resource_initial_ids, new_ids_for_resource
        )
        has_perm = has_perm or has_group_diff_perm

    return has_perm


def permission_required(viewset_function):
    """
    Decorator (specifically made for viewset functions) that checks whether a 'user' can do 'action' on 'resource'.
    Calls the viewset function if the user has permission to do so.
    Other permission decorators that are not directly related to the ACL system can be found in base.decorators.
    """

    def permission_check_wrapper(self, request, *args, pk=None, **kwargs):
        # First check if the user has the permission (even anon users)
        user = request.user
        action = self.action
        resource_model = self.get_queryset().model

        # We use a middleware that adds an 'is_internal' attribute in the request object if this is a request that
        # comes from another docker container behind the nginx reverse proxy. Those requests are always
        # granted all the rights.
        if getattr(request, 'is_master_api_key', None):
            has_perm = True
        # If the user is not logged in, raise a NotAuthenticated exception
        elif not getattr(request, "user", None):
            raise NotAuthenticated("user_not_authenticated")
        # If this is a normal request with a logged in user coming from the frontend, do the normal permission check.
        else:
            has_perm = user_has_permission(request, user, action, pk=pk, resource_model=resource_model)

        # Go ahead only if user has_perm, else raise a 403 error
        if has_perm:
            if "pk" in signature(viewset_function).parameters.keys():
                kwargs["pk"] = pk
            return viewset_function(self, request, *args, **kwargs)
        else:
            raise PermissionDenied("user_does_not_have_permission")

    return permission_check_wrapper
