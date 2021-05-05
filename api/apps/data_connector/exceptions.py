"""This is where we define all exceptions related to the startup backend connector.
Exceptions are raised in the modules in charge of the business logic.
They are catched in views_v1.py.
"""
from rest_framework.exceptions import APIException


class StartupApiError(APIException):
    status_code = 500
    default_detail = "Error on the Startup API side. Go check the logs from the Startup API."
    default_code = "startup_api_error"


class StartupApiConnectionError(APIException):
    http_status_code = 500
    default_detail = "Could not communicate with Startup API."
    default_code = "startup_api_connection_error"


class DataConnectorError(APIException):
    http_status_code = 500
    default_detail = "Startup API returned status code != 200. Go check its logs."
    default_code = "data_connector_error"
