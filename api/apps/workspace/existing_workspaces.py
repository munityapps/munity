"""
    This class was isolated here to solve a dependency problem. 
    settings.py needs it on project startup while the models are not yet loaded, so we cannot put this class inside
    operations.py along with all the others.
"""
import psycopg2


class ExistingWorkspace(object):
    """
    Singleton factory for the class __ExistingWorkspace
    """

    class __ExistingWorkspace:
        """
        Singleton class. Avoid to recreate a new connection DB each time.
        Usefull to list all existing workspaces.
        """

        def __init__(self, db_user, db_host, db_password, db_name="postgres"):
            self.init_params = {"db_user": db_user, "db_host": db_host, "db_password": db_password, "db_name": db_name}
            self.db_connection = psycopg2.connect(
                f"dbname={db_name} user='{db_user}' host='{db_host}' password='{db_password}'"
            )

        def list_existing_workspaces(self):
            """CAUTION: This returns workspace_db_names, not workspace_slugs."""

            try:
                cur = self.db_connection.cursor()
            except psycopg2.InterfaceError:
                self.__init__(**self.init_params)
                cur = self.db_connection.cursor()

            cur.execute("""SELECT datname from pg_database;""")
            rows = cur.fetchall()

            workspace_database_names = [row[0] for row in rows if row[0].startswith("workspace_")]
            cur.close()
            return workspace_database_names

        def __del__(self):
            self.db_connection.close()

    instance = None

    def __new__(cls, db_user, db_host, db_password, db_name="postgres"):
        if not ExistingWorkspace.instance:
            ExistingWorkspace.instance = ExistingWorkspace.__ExistingWorkspace(db_user, db_host, db_password, db_name)
        return ExistingWorkspace.instance
