import re
import json
from uuid import UUID

class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return obj.hex
        return json.JSONEncoder.default(self, obj)

def get_request_info(request):
    # return (workspace_slug, ressource_type, action)

    if (request.method == "GET"):
        action = "list"
    if (request.method in ["PATCH", "PUT"]):
        action = "update"
    if (request.method == "DELETE"):
        action = "delete"
    if (request.method == "POST"):
        action = "create"

    ask_for_all_ws = re.search('^\/v[0-9]+\/workspaces/$', request.path)
    if (ask_for_all_ws) :
        return (None, "workspaces", action)

    ask_for_specific_ws = re.search('^\/v[0-9]+\/workspaces/([^\/]+)/$', request.path)
    if (ask_for_specific_ws) :
        return (ask_for_specific_ws.group(1), "workspaces", action)

    ask_for_specific_ws_ressource = re.search('^\/v[0-9]+\/workspaces/([^\/]+)\/([a-z\-]+)\/', request.path)
    if (ask_for_specific_ws_ressource) :
        return (ask_for_specific_ws_ressource.group(1), ask_for_specific_ws_ressource.group(2), action)

    ask_for_all_ressource = re.search('^\/v[0-9]+\/([^\/]+)\/', request.path)
    if (ask_for_all_ressource) :
        return (None, ask_for_all_ressource.group(1), action)
