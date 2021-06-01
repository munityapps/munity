import logging
import os
from logging.handlers import RotatingFileHandler


class Logger:
    """
        Print logs in console and write on file /logs/{{workspace_slug}}.log
        Logs are written in separate files according to the workspace.

        Logger usage:
            from base.logs import get_logger

            log = get_logger(workspace_slug)

            log.info('Log %s', 'arguments')
            log.warning('Warning')
            log.debug('Debug')
            log.error('Error')
            log.critical('Critical')
    """

    class __Logger:
        def __init__(self):
            self.loggers = {}

    instance = None

    def __init__(self):
        if not Logger.instance:
            Logger.instance = Logger.__Logger()
        else:
            pass

    def get(self, workspace_slug=None):
        """Get a workspace-specific logger."""
        # If no workspace_slug is specified, use "general" as default workspace_slug
        workspace_slug = workspace_slug if workspace_slug is not None else "general"
        # If there is already a logger for this workspace, return it. Else, create a new one.
        if not self.instance.loggers.get(workspace_slug):
            # Set up the logs folder if necessary
            logs_folder_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "logs"
            )
            log_filename = f"{workspace_slug}.log"
            try:
                os.makedirs(logs_folder_path, exist_ok=True)
            except TypeError:
                os.makedirs(logs_folder_path)

            # Create the logger and associate a level to it
            # Reference: http://sametmax.com/ecrire-des-logs-en-python/
            # Also, find the documentation for the logging module here: https://docs.python.org/3/library/logging.html
            logger = logging.getLogger(workspace_slug)
            logger.setLevel(logging.DEBUG)

            # Create a custom log string formatter
            formatter = logging.Formatter(f"%(asctime)s :: {workspace_slug} :: %(levelname)s :: %(message)s")

            # Below we attach a handlers to the logger:
            # RotatingFileHandler: Writes rotating logs to a file
            file_handler = RotatingFileHandler(os.path.join(logs_folder_path, log_filename), "a", 8_000_000, 1)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

            # StreamHandler: Writes logs to the console
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(formatter)
            logger.addHandler(stream_handler)

            self.instance.loggers[workspace_slug] = logger
        else:
            # Return the instance of the workspace logger
            logger = self.instance.loggers.get(workspace_slug)
        return logger


def get_logger(*args, **kwargs):
    return Logger().get(*args, **kwargs)
