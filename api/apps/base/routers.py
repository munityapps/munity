import copy

from rest_framework_bulk.routes import BulkRouter


class SingleObjectRouter(BulkRouter):
    routes = copy.deepcopy(BulkRouter.routes)
    routes[0].mapping.update({"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"})


class LazySingleObjectCreateOrUpdateRouter(BulkRouter):
    routes = copy.deepcopy(BulkRouter.routes)
    routes[0].mapping.update(
        {
            "get": "get_or_create",
            "post": "update_or_create",
            "put": "update_or_create",
            "patch": "partial_update",
            "delete": "destroy",
        }
    )
