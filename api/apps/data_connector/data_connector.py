import json
import time
from datetime import datetime

import requests
from django.conf import settings


def get_device_data(
    devices,
    is_last_value: bool,
    data_types: list = None,
    from_timestamp: datetime = None,
    to_timestamp: datetime = None,
    aggregate_period_name: str = None,
    aggregate_operation_name: str = None,
    decimal_places: int = None,
):
    # All values are optional
    if not devices:
        return []

    if isinstance(from_timestamp, datetime):
        from_timestamp = from_timestamp.isoformat()
    if isinstance(to_timestamp, datetime):
        to_timestamp = to_timestamp.isoformat()

    data_dict = {
        "devices": devices,
        "is_last_value": is_last_value,
        "data_types": data_types,
        "from_timestamp": from_timestamp,
        "to_timestamp": to_timestamp,
        "aggregate_period_name": aggregate_period_name,
        "aggregate_operation_name": aggregate_operation_name,
        "decimal_places": decimal_places,
    }

    if settings.DEBUG:
        time1 = time.time()
    # Exceptions are not caught to help with the debugging
    try:
        startup_response = requests.post(
            f"{settings.STARTUP_API_URL}/device_data",
            data=json.dumps(data_dict),
            headers={"Content-Type": "application/json", "Authorization": f"APIKEY {settings.STARTUP_API_API_KEY}"},
        )
        startup_response.raise_for_status()
    except:
        raise Exception(f"Cannot get devices data from startup api")
    try:
        startup_response.raise_for_status()
    except:
        raise Exception(f"Error {startup_response.status_code} calling the Startup API: {startup_response.text}")

    if settings.DEBUG:
        time2 = time.time()
        print("Handling the startup API request took ", (time2 - time1), " s ")

    startup_response_serialized = startup_response.json()

    # put back device name in result
    if isinstance(devices, dict):
        result = []
        for data_point in startup_response_serialized:
            data_point['name'] = devices[data_point['reference']]
            result.append(data_point)
        return result
    else:
        return startup_response_serialized
