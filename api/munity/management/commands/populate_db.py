import random

import requests
from django.conf import settings
from django.core import management
from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from accounts.models import User, UserGroupMembership
from acl.models import GroupRole, WorkspaceRole
from devices.models import Device
from dynamic_db_router import in_database
from groups.models import Group
from munity.settings_acl import DefaultGroupRoleChoice, DefaultWorkspaceRoleChoice

@atomic  # NOQA: C901
def _populate_db(workspace_slug="default"):
    # Retrieve Workspace Roles
    w_role_Owner, __ = WorkspaceRole.objects.get_or_create(workspace_role_name=DefaultWorkspaceRoleChoice.OWNER.value)
    w_role_Admin, __ = WorkspaceRole.objects.get_or_create(workspace_role_name=DefaultWorkspaceRoleChoice.ADMIN.value)
    w_role_User, __ = WorkspaceRole.objects.get_or_create(workspace_role_name=DefaultWorkspaceRoleChoice.USER.value)

    # Retrieve Group Roles
    g_role_Admin, __ = GroupRole.objects.get_or_create(group_role_name=DefaultGroupRoleChoice.ADMIN.value)
    g_role_User, __ = GroupRole.objects.get_or_create(group_role_name=DefaultGroupRoleChoice.USER.value)
    group_roles = [g_role_Admin, g_role_User]

    # Create users with workspace_roles
    if User.objects.filter(username="marisella@munityapps.com").first() == None:
        marisella = User.objects.create_user(
            first_name="Marisella",
            last_name="Pacheco",
            username="marisella@munityapps.com",
            email="marisella@munityapps.com",
            password="Password1$",
            is_superuser=True,
            is_staff=True,
            workspace_role=w_role_Owner,
        )
    else:
        marisella = User.objects.get(username="marisella@munityapps.com")

    if User.objects.filter(username="cyril@munityapps.com").first() == None:
        cyril = User.objects.create_user(
            first_name="Cyril",
            last_name="Alfaro",
            username="cyril@munityapps.com",
            email="cyril@munityapps.com",
            password="Password1$",
            workspace_role=w_role_Admin,
        )
    else:
        cyril = User.objects.get(username="cyril@munityapps.com")

    if User.objects.filter(username="martin@munityapps.com").first() == None:
        martin = User.objects.create_user(
            first_name="Martin",
            last_name="Perreau",
            username="martin@munityapps.com",
            email="martin@munityapps.com",
            password="Password1$",
            workspace_role=w_role_User,
        )
    else:
        martin = User.objects.get(username="martin@munityapps.com")
    users = [marisella, cyril, martin]

    headers = {"Content-Type": "application/json", "Authorization": f"APIKEY {settings.STARTUP_API_API_KEY}"}
    print(f"Import from URL {settings.STARTUP_API_URL}{settings.STARTUP_API_DEVICES_URL}")
    devices_raw = requests.get(f"{settings.STARTUP_API_URL}{settings.STARTUP_API_DEVICES_URL}", headers=headers)
    print("RAWS Data", devices_raw)
    devices = devices_raw.json()

    # CREATE GROUPS
    groups = [Group.objects.get_or_create(name="Group_" + str(num))[0] for num in range(1, 11)]
    # Associate Users with Groups and a GroupRole within the group
    for user in users[:-1]:
        for _ in range(random.randint(0, 4)):
            __, __ = UserGroupMembership.objects.get_or_create(
                user=user, group=random.choice(groups), defaults={"group_role": random.choice(group_roles)}
            )

    if devices:
        device_names = [device["id"] for device in devices]
        print("NAMES", device_names)

        devices = [
            Device.objects.get_or_create(device_name=device_name, device_reference=device_name)[0]
            for device_name in device_names
        ]
        for device in devices:
            if random.randint(0, 2) > 1:
                device.groups.add(Group.objects.get_or_create(name="Group_" + f"{random.randint(1, 11)}")[0])


class Command(BaseCommand):
    help = "Populates a database with some entries"

    def add_arguments(self, parser):
        parser.add_argument("workspace_slug", nargs="+", type=str)

    def handle(self, *args, **options):
        workspace_slug = options["workspace_slug"][0].replace("_", "-")
        with in_database(workspace_slug, write=True):
            _populate_db(workspace_slug)
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully populated database "workspace_{workspace_slug}" for workspace "{workspace_slug}".'
            )
        )
