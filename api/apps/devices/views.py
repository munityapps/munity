# LIBS
import copy
import json
import uuid

# DJANGO
from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from rest_framework import status
from rest_framework.decorators import action, api_view
from rest_framework.exceptions import ParseError, PermissionDenied, ValidationError
from rest_framework.response import Response

from acl.operations import has_workspace_permission
from base.viewsets import MultipleDBModelViewSet
from data_connector import data_connector
from devices.models import Device, log_bulk_change
from devices.operations import (
    get_references_from_ids,
    hardware_ids_from_api_by_workspace_slug,
    hardwares_assignment,
    engine_inactive_group,
    check_hardwares_assignment,
)

from devices.serializers import DeviceSerializer
from graphs.models import PreviewSettings
from graphs.serializers import PreviewSettingsSerializer
from groups.models import Group
from logs.models import Log


class DeviceViewSet(MultipleDBModelViewSet):
    serializer_class = DeviceSerializer
    queryset = Device.objects.none()

    def get_queryset(self):
        queryset = Device.objects

        # Retrieve query parameters
        ids = json.loads(self.request.query_params.get("ids", "{}"))

        # Filter according to query parameters
        if ids:
            queryset = queryset.filter(groups__id__in=ids)
        elif ids != {}:
            queryset = queryset.filter(groups__isnull=True)

        # Filter according to what the user has permission to see
        if has_workspace_permission(self.request.user, self.action, self.queryset.model.__name__, self.request):
            # Someone who has workspace permission to GET Devices, can see all Devices inluding those that have id=None
            pass
        else:
            # Else, someone can only see Devices among those that belong to groups they have access to,
            # so we are filtering further: we are only returning the devices that are in
            # at least one of the groups the user is in
            user_groups = self.request.user.groups.all()
            queryset = queryset.filter(groups__in=user_groups).distinct()
        return queryset.prefetch_related("groups")

    def update(self, request, *args, pk=None, **kwargs):

        device = self.get_object()

        all_workspaces_devices = hardware_ids_from_api_by_workspace_slug(request.workspace_slug)
        reference = get_references_from_ids(user=request.user, ids=[device.id], request=request)[0]

        devices_hardwares = []
        for device_to_check_hw in all_workspaces_devices:
            if device_to_check_hw["reference"] == reference:
                devices_hardwares = device_to_check_hw
                break

        super().update(request, *args, pk=pk, **kwargs)
        device_hw_id_by_ref = {}
        hw_ids = request.data.get("hardware_ids")
        if hw_ids is not None:
            hardwares_to_reassign = [{"hardware_ids": hw_ids}]
            device_to_update = {reference: hw_ids}

            device_hw_id_by_ref = check_hardwares_assignment(
                request.workspace_slug, hardwares_to_reassign, all_workspaces_devices
            )
            if hardwares_to_reassign:
                status_code, hardware_ids_removed = hardwares_assignment(
                    request.workspace_slug, device_hw_id_by_ref
                )
                status_code, hardware_ids_updated = hardwares_assignment(request.workspace_slug, device_to_update)

                devices_hardwares = [hardware_ids_updated]
                devices = [device]

                if hardware_ids_removed:
                    devices = [
                        device,
                        Device.objects.get(reference=hardware_ids_removed["reference"]),
                    ]
                    devices_hardwares = [hardware_ids_updated, hardware_ids_removed]
                    Log(
                        action_type="UPDATE",
                        modified_model_name="Device",
                        modified_object_name=devices[1].reference,
                        modified_object_id=devices[1].id,
                        modification={
                            "new": {
                                "hardware_ids": hardware_ids_removed["hardware_ids"]
                                if len(hardware_ids_removed["hardware_ids"]) > 0
                                else ""
                            },
                            "old": {"hardware_ids": hw_ids},
                        },
                    ).save()

                Log(
                    action_type="UPDATE",
                    modified_model_name="Device",
                    modified_object_name=device.reference,
                    modified_object_id=device.id,
                    modification={
                        "new": {"hardware_ids": devices_hardwares[0]["hardware_ids"]},
                        "old": {"hardware_ids": device_to_check_hw["hardware_ids"] if device_to_check_hw else ""},
                    },
                ).save()

        devices_updated_refs = list(device_hw_id_by_ref.keys())
        devices_updated_refs.append(self.get_object().reference)

        devices_updated = Device.objects.filter(reference__in=devices_updated_refs)

        serializer = self.get_serializer(devices_updated, many=True)
        response_serializer = serializer.data

        self.query_device_data(devices_updated, response_serializer)

        return Response(data=response_serializer)

    def list(self, request, page=None, step=None):

        queryset = self.get_queryset()

        # Reading "count_only" URL query param
        if json.loads(self.request.query_params.get("count_only", "false")) is True:
            return Response({"count": queryset.count()})
        serializer = self.get_serializer(queryset, many=True)
        devices = Device.objects.filter(pk__in=[element["id"] for element in serializer.data])

        references = get_references_from_ids(
            user=request.user, ids=[device.id for device in devices], request=request
        )

        # Query the Startup API endpoint
        try:
            device_data = data_connector.get_device_data(
                devices=references, is_last_value=True, data_types=settings.DATA_TYPES_TO_LOAD
            )
        except Exception as e:
            device_data = []

        for element in serializer.data:
            device = next((device for device in devices if str(device.id) == element["id"]), None)
            element["hardware_ids"] = []
            element["data"] = []
            for data in device_data:
                if data.get("reference", "") == device.reference:
                    element["data"].append(data)
                    if data.get("data_type") == "hardware_ids":
                        hw_ids = data["data_points"][0]["value"]
                        element["hardware_ids"] = hw_ids
        # =========Pagination===========
        if step == None:
            step = settings.PAGE_SIZE
        count = len(serializer.data)
        if page is not None:
            # Pagination
            paginator = Paginator(serializer.data, step)
            try:
                return Response(data={"count": count, "results": list(paginator.get_page(page))})
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                return Response(data=[])

        return Response(serializer.data)

    def partial_bulk_update(self, request, pk=None, *args, **kwargs):
        if "ids" not in request.data:
            raise ParseError("you_must_specify_the_ids_parameter")
        if "ids" not in request.data:
            raise ParseError("you_must_specify_the_ids_parameter")

        ids = request.data.get("ids")
        ids = request.data.get("ids")

        groups = Group.objects.filter(pk__in=ids)
        # We have to do it like this because the frontend wants to use the same endpoint for adding or removing groups.
        # Ideally we should have two endpoints but I'm leaving it like that
        for group in groups:
            devices_in_group = Device.objects.filter(pk__in=ids).filter(groups=group)
            devices_not_in_group = tuple(Device.objects.filter(pk__in=ids).exclude(groups=group))

            if devices_in_group:
                Device.groups.through.objects.filter(group=group, device__in=devices_in_group).delete()

            if devices_not_in_group:
                Device.groups.through.objects.bulk_create(
                    [Device.groups.through(device=device, group=group) for device in devices_not_in_group]
                )

        updated_devices = Device.objects.filter(pk__in=ids).prefetch_related("groups")
        serializer = DeviceSerializer(updated_devices, many=True)
        return Response(data=serializer.data)

    def create(self, request, *args, **kwargs):
        # Get data from request
        devices_to_insert = request.data["devices"]

        all_workspaces_devices = hardware_ids_from_api_by_workspace_slug(request.workspace_slug)

        # Remove Hardwares Assignment
        device_hw_id_by_ref = check_hardwares_assignment(
            request.workspace_slug, devices_to_insert, all_workspaces_devices
        )
        hardwares_assignment(request.workspace_slug, device_hw_id_by_ref)
        # Create new devices
        devices_to_create = []
        devices_to_insert_ref = []
        device_ref_by_groups_ids = {}
        for device in devices_to_insert:
            device_to_insert_ref = str(uuid.uuid4())
            devices_to_insert_ref.append(device_to_insert_ref)

            # Create devices in MUNITY
            new_device = Device(reference=device_to_insert_ref)
            for k, v in device.items():
                if k != "groups":
                    setattr(new_device, k, v)

            devices_to_create.append(new_device)

            # Create and send new devices in API STARTUP
            device_in_api_startup = {
                new_device.reference: device["hardware_ids"],
                "defaults": {k: v for k, v in device.items()},
            }
            if "hardware_ids" in device.keys():
                del device_in_api_startup["defaults"]["hardware_ids"]

            # Update Hardwares Assignment
            hardwares_assignment(request.workspace_slug, device_in_api_startup)
            if "ids" in device.keys():
                device_ref_by_groups_ids[device_to_insert_ref] = device["ids"]

        # Save new devices with bulk db method
        if len(devices_to_create) > 0:
            Device.objects.bulk_create(devices_to_create, len(devices_to_create))
            log_bulk_change(devices_to_create, "CREATE")

        devices_created = Device.objects.filter(reference__in=devices_to_insert_ref)

        # Add groups for all device created
        for device_created in devices_created:
            if device_created.reference in device_ref_by_groups_ids:
                groups_to_add = Group.objects.filter(
                    id__in=device_ref_by_groups_ids[device_created.reference]
                )
                Device.groups.through.objects.bulk_create(
                    [Device.groups.through(device=device_created, group=group_to_add) for group_to_add in groups_to_add]
                )

        device_updated_refs = list(device_hw_id_by_ref.keys())
        device_updated_refs.extend(devices_to_insert_ref)

        devices_updated = Device.objects.filter(reference__in=device_updated_refs)

        engine_inactive_group(devices_updated, hardware_ids_from_api_by_workspace_slug(request.workspace_slug))

        serializer = self.get_serializer(devices_updated, many=True)

        response_serializer = self.query_device_data(devices_updated, serializer.data)

        return Response(data=response_serializer)

    def query_device_data(self, devices, response_serializer):

        request = self.request

        references = get_references_from_ids(
            user=request.user, ids=[device.id for device in devices], request=request
        )

        # Query the Startup API endpoint
        try:
            device_data = data_connector.get_device_data(
                devices=references, is_last_value=True, data_types=settings.DATA_TYPES_TO_LOAD
            )
        except Exception as e:
            print(e)
            device_data = []

        for element in response_serializer:
            device = next((device for device in devices if str(device.id) == element["id"]), None)
            element["hardware_ids"] = None
            element["data"] = []
            for data in device_data:
                if data.get("reference", "") == device.reference:
                    element["data"].append(data)
                    if data.get("data_type") == "hardware_ids":
                        hw_ids = data["data_points"][0]["value"]
                        element["hardware_ids"] = hw_ids

        return response_serializer

    @action(detail=True)
    def preview(self, *args, **kwargs):
        # We embed the __preview function like so as a workaround because it seems we can't combine
        # the @action decorator with another decorator (@workspace_specific)
        def __preview(self, request, pk=None):
            """Return Device PreviewSettings and Device Data at the same time."""

            # Fetch actual PreviewSettings
            preview_settings = PreviewSettings.objects.get(pk=pk)
            previewsettings_serializer = PreviewSettingsSerializer(preview_settings)
            # rearranging output data for the front end
            """
            "ids": [
                            "13ad6743-0b2f-4030-9294-0a604712ba5c"
                        ]
            """
            ps = previewsettings_serializer.data
            ps["ids"] = [previewsettings_serializer.data["id"]]
            ps.pop("id", None)
            # Fetch Device Data
            device = Device.objects.get(pk=pk)
            graph_data = device.get_device_data(data_types="__all__", is_last_value=False)  # NOQA: F841

            # Return both PreviewSettings and Device Data
            return Response({"preview_settings": ps})

        return __preview(self, *args, **kwargs)

    @action(detail=False, methods=["POST"], url_path="import")
    def import_devices(self, request, *args, **kwargs):
        def __import_devices(self, request, *args, **kwargs):
            """
            Import devices in bulk.
            This was originally meant to be called from Lumber, but you can reuse it.

            Usage example:
            requests.post(
                url='http://api/v1/import-devices/',
                headers={'content-type': 'application/json', 'authorization': 'Bearer {{token}}'},
                data=json.dumps({
                    'workspace': {{workspace_slug}},
                    'devices': [{
                        reference: {{reference}},
                        name: {{name}},
                        address: {{address}},
                        position: {{position}},
                        description: {{description}}
                    }]
                })
            )
            """
            # Get data from request
            devices_to_upsert = request.data["devices"]
            devices_to_upsert_ref = [device["reference"] for device in request.data["devices"]]

            # Find data from db
            devices_present = Device.objects.filter(reference__in=devices_to_upsert_ref)

            devices_present_ref = [device.reference for device in devices_present]

            # Filter device to update or insert
            devices_to_update = [
                device for device in devices_to_upsert if device["reference"] in devices_present_ref
            ]
            devices_to_insert = [
                device for device in devices_to_upsert if device["reference"] not in devices_present_ref
            ]

            # Create or update devices
            devices_to_create = []
            for device in devices_to_insert:
                new_device = Device(reference=device["reference"])
                for k, v in device.items():
                    setattr(new_device, k, v)
                devices_to_create.append(new_device)
            devices_to_save = []
            old_devices_to_save = []
            for device in devices_to_update:
                device_to_update = None
                for device_present in devices_present:
                    if device_present.reference == device.get("reference"):
                        device_to_update = device_present
                        break
                old_devices_to_save.append(copy.deepcopy(device_to_update))
                for k, v in device.items():
                    setattr(device_to_update, k, v)
                devices_to_save.append(device_to_update)

            # Save devices with bulk db method
            if len(devices_to_create) > 0:
                device = Device.objects.bulk_create(devices_to_create, len(devices_to_create))
                log_bulk_change(devices_to_create, "CREATE")
                device.save()
            if len(devices_to_save) > 0:
                Device.objects.bulk_update(devices_to_save)
                log_bulk_change(devices_to_save, "UPDATE", old_devices_to_save)

            return Response(status=status.HTTP_201_CREATED)

        return __import_devices(self, request, *args, **kwargs)


@api_view(["GET"])
def get_all_hardware_ids(request):
    return Response(hardware_ids_from_api_by_workspace_slug(request.workspace_slug))


@api_view(["GET"])
def device_summary(request, id, page):
    if id is None:
        raise ValidationError("missing_params")
    # Get log list associated with device
    logs = (
        Log.objects.filter(modified_object_id=id)
        .order_by("-created_at")
        .values(
            "username",
            "action_type",
            "modified_model_name",
            "modified_object_name",
            "name",
            "role_name",
            "workspace_name",
            "created_at",
            "modification",
            "modified_object_id",
            "user_id",
        )
    )
    # Pagination
    paginator = Paginator(logs, settings.PAGE_SIZE)
    try:
        out_logs = list(paginator.get_page(page))
    except PageNotAnInteger:
        # If page is not an integer, raise exception
        ValidationError("page_number_invalid")
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        return Response(data=[])
    count = logs.count()
    return Response(data={"count": count, "summary": out_logs})
