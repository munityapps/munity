import requests
import json
from acl.operations import has_workspace_permission
from devices.models import Device
from groups.models import Group
from django.conf import settings
from workspace.operations import list_existing_workspaces
from workspace.utils import db_name_to_slug


def get_references_from_ids(user, ids, request_is_internal=False, request=None):
    """
        get device references from a list of ids if the user has good right on devices.
    """
    queryset = Device.objects.filter(pk__in=ids)
    if request_is_internal or has_workspace_permission(user, "retrieve", queryset.model.__name__, request):
        # Someone who has workspace permission to GET Devices, can see all Devices inluding those that have id=None
        pass
    else:
        # Else, someone can only see Devices among those that belong to groups they have access to,
        # so we are filtering further: we are only returning the devices that are in
        # at least one of the groups the user is in
        user_groups = user.groups.all()
        queryset = queryset.filter(groups__in=user_groups).distinct()
    devices_reference = [device.reference for device in queryset]

    return devices_reference


def check_devices_for_inactive_group(devices, devices_hardwares):
    devices_in_inactive_group = []
    for device in devices:
        for device_to_check_hw in devices_hardwares:
            if device_to_check_hw["reference"] == device.reference:
                if not device_to_check_hw["hardware_ids"]:
                    devices_in_inactive_group.append(device)
                    break
    return devices_in_inactive_group


def add_remove_devices_for_inactive_group(devices_in_inactive_group):

    # Remove devices_in_inative_group of all groups
    for device in devices_in_inactive_group:
        groups = device.get_associated_groups()
        for group in groups:
            device.groups.remove(group)

    # Add devices_in_inative_group in inactive_group
    inactive_group_uuid = settings.INACTIVE_GROUP_UUID
    inactive_group_exist = Group.objects.filter(id=inactive_group_uuid).count()
    if inactive_group_exist:
        group_inactive = Group.objects.get(id=inactive_group_uuid)
        Device.groups.through.objects.bulk_create(
            [Device.groups.through(device=device, group=group_inactive) for device in devices_in_inactive_group]
        )


def engine_inactive_group(devices, devices_hardwares):

    if settings.INACTIVE_GROUP:
        # Create Group inactive if no exist
        inactive_group_uuid = settings.INACTIVE_GROUP_UUID
        group_inactive_exist = Group.objects.filter(name=settings.INACTIVE_GROUP_NAME).count()
        if not group_inactive_exist:
            Group.objects.create(pk=inactive_group_uuid, name=settings.INACTIVE_GROUP_NAME)

        devices_in_inactive_group = check_devices_for_inactive_group(devices, devices_hardwares)
        add_remove_devices_for_inactive_group(devices_in_inactive_group)

    return devices_in_inactive_group


def check_hardwares_assignment(workspace_slug, devices, all_workspaces_devices):
    # Update hardware_ids in startup api
    device_hw_id_by_ref = {}
    for workspace_device in all_workspaces_devices:
        reference = workspace_device["reference"]
        hardware_ids = workspace_device["hardware_ids"]
        workspaces_slugs = workspace_device["workspaces_slugs"]
        device_hw_id_by_ref[reference] = hardware_ids
        have_to_update = False
        for device in devices:
            for hw_id in device["hardware_ids"]:
                if hw_id in hardware_ids and hw_id != []:
                    if (workspace_slug in workspaces_slugs) or (len(workspaces_slugs) == 0):
                        device_hw_id_by_ref[reference].remove(hw_id)
                        have_to_update = True
                    else:
                        devices.remove(device)

        if not have_to_update:
            del device_hw_id_by_ref[reference]

    return device_hw_id_by_ref


def hardwares_assignment(worksapce_slug, device_hw_id_by_ref):

    status_code = False
    data = False
    # Update hardware_ids in startup api
    if bool(device_hw_id_by_ref):
        status_code, response = update_hw_ids_in_api_startup(worksapce_slug, device_hw_id_by_ref) reference = list(response.keys())[0]
        data = {"reference": reference, "hardware_ids": response[reference]}
    return status_code, data


def update_hw_ids_in_api_startup(worksapce_slug, device_to_update):
    try:
        startup_response = requests.post(
            f"{settings.STARTUP_API_URL}/device_hardware_ids",
            data=json.dumps(device_to_update),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"APIKEY {settings.STARTUP_API_API_KEY}",
                "workspace_slug": worksapce_slug,
            },
        )
    except:
        raise Exception(f"Cannot set hardware ids data to startup api")
    try:
        startup_response.raise_for_status()
    except:
        raise Exception(f"Error {startup_response.status_code} calling the Startup API: {startup_response}")
    return startup_response.status_code, startup_response.json()


def hardware_ids_from_api_by_workspace_slug(my_workspace_slug):

    db_names = list_existing_workspaces()

    devices_references_from_munity = {}
    for db_name in db_names:
        workspace_slug = db_name_to_slug(db_name)
        devices = Device.objects.using(workspace_slug).all()
        for device in devices:
            if device.reference in devices_references_from_munity.keys():
                devices_references_from_munity[device.reference].append(workspace_slug)
            else:
                devices_references_from_munity[device.reference] = [workspace_slug]

    headers = {"Content-Type": "application/json", "Authorization": f"APIKEY {settings.STARTUP_API_API_KEY}"}
    devices_raw = requests.get(f"{settings.STARTUP_API_URL}{settings.STARTUP_API_DEVICES_URL}", headers=headers)
    devices = devices_raw.json()
    devices_from_api_startup = []
    for device in devices:
        workspaces_slugs = []
        if device["id"] in devices_references_from_munity.keys():
            workspaces_slugs = devices_references_from_munity[device["id"]]
        if (my_workspace_slug in workspaces_slugs) or (len(workspaces_slugs) == 0):
            device_from_api_startup = {
                "reference": device["id"],
                "workspaces_slugs": workspaces_slugs,
                "hardware_ids": device["hardware_ids"],
            }

            devices_from_api_startup.append(device_from_api_startup)

    return devices_from_api_startup
