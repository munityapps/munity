from devices.models import Device
from groups.models import Group
from accounts.models import User, UserGroupMembership
from acl.models import GroupRole
from rest_framework.exceptions import NotFound


def add_remove_devices(group, ids):
    # Add/Remove devices from group
    try:
        if ids != None:
            for device in group.devices.all():
                if str(device.id) not in ids:
                    device.groups.remove(group)
            for id in ids:
                device = Device.objects.get(pk=id)
                if group not in device.groups.all():
                    device.groups.add(group)
    except Device.DoesNotExist:
        NotFound("group_not_found")
        raise Exception(f"Cannot get devices from ids")

    return True


def add_remove_groups(group, ids):
    try:
        # Add/Remove groups from group
        if ids != None:
            for group_to_remove in group.groups.all():
                if str(group_to_remove.id) not in ids:
                    group.groups.remove(group_to_remove)
            for group_to_add_id in ids:
                group_to_add = Group.objects.get(id=group_to_add_id)
                if group_to_add not in group.groups.all():
                    group.groups.add(group_to_add)
    except Group.DoesNotExist:
        NotFound("group_not_found")
        raise Exception(f"Cannot get groups from ids")

    return True


def add_remove_users(group, users):
    try:
        # Add/Remove users from group
        if users != None:
            users_to_add = []
            for user in users:
                users_to_add.append(user["id"])
                user_to_add = User.objects.get(id=user["id"])
                if user_to_add not in group.members.all():
                    group_role = GroupRole.objects.get(pk=user["role_id"])
                    UserGroupMembership(user=user_to_add, group=group, group_role=group_role).save()

            for user_to_remove in group.members.all():
                if str(user_to_remove.id) not in users_to_add:
                    UserGroupMembership.objects.filter(user_id=user_to_remove.id, id=group.id).delete()

    except User.DoesNotExist:
        NotFound("user_not_found")
        raise Exception(f"Cannot get users from user_ids")

    return True
