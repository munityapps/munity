from devices.models import Device, Group
from devices.operations import get_references_from_ids
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from . import data_connector


"""

IMPORTANT NOTE:
---------------

Isolating data per workspace with the @workspace_specific and @workspace_specific_for_api_view decorators DOES NOT WORK
when making requests to the Startup API because we are calling an external API, not performing operations directly on database models.
Additional security controls are necessary (see get_graph_data for example).

"""


@api_view(["POST"])
def get_data_types_for_devices(request):
    ids = request.data.get("ids")
    id = request.data.get("id")
    if id:
        # Check request parameters
        group = Group.objects.get(pk=id)
        ids = [device.id for device in group.get_related_devices()]

    if not ids:
        return Response({"message": "devices_not_specified"}, status=status.HTTP_403_FORBIDDEN)

    references_and_names = get_references_from_ids(user=request.user, ids=ids)
    if not references_and_names:
        return Response({"message": "bad_rights_for_devices"}, status=status.HTTP_403_FORBIDDEN)

    # Query the Startup API endpoint
    device_data = data_connector.get_device_data(
        devices=references_and_names, is_last_value=True, data_types=["__all__"]
    )
    # Process the response
    try:
        data_types = list(set([x.get("data_type") for x in device_data]))
    except Exception as e:
        data_types = []
        print(e)

    # Return the processed response
    return Response({"data": data_types})



@api_view(["POST"])
def get_graph_data(request):

    # Check request parameters
    ids = request.data.get("ids")
    if not ids:
        return Response({"message": "devices_not_specified"}, status=status.HTTP_403_FORBIDDEN)

    # Check that all ids are actually stored in the workspace (otherwise we would let users fetch data from devices in other workspaces)
    if Device.objects.filter(pk__in=ids).count() < len(ids):
        raise PermissionDenied("user_does_not_have_permission")

    references_and_names = get_references_from_ids(
        user=request.user, ids=request.data["ids"]
    )
    if not references_and_names:
        return Response({"message": "bad_rights_for_devices"}, status=status.HTTP_403_FORBIDDEN)

    # Query the Startup API endpoint
    graph_data = data_connector.get_device_data(
        devices=references_and_names,
        is_last_value=request.data.get("is_last_value", False),
        data_types=request.data.get("device_data_types", ["__all__"]),
        from_timestamp=request.data.get("from_timestamp"),
        to_timestamp=request.data.get("to_timestamp"),
        aggregate_period_name=request.data.get("aggregate_period_name"),
        aggregate_operation_name=request.data.get("aggregate_operation_name"),
        decimal_places=request.data.get("decimal_places"),
    )

    return Response({"data": graph_data})

