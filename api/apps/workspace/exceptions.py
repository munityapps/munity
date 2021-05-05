"""This is where we define all exceptions related to workspace.
Exceptions are raised in the modules in charge of the business logic.
They are catched in views_v1.py.
"""

class WorkspaceCreationError(Exception):
    http_status_code = 500

    def __str__(self):
        return self.__class__.__name__

class InvalidWorkspaceNameError(WorkspaceCreationError):
    http_status_code = 400


class DatabaseAlreadyExistsError(WorkspaceCreationError):
    http_status_code = 400


class CreateDatabaseError(WorkspaceCreationError):
    http_status_code = 500
