def db_name_to_slug(workspace_db_name):
    """workspace_db_name -> workspace_slug"""
    return workspace_db_name[len("workspace_") :].replace("_", "-")


def slug_to_db_name(workspace_slug):
    """workspace_slug -> workspace_db_name"""
    return f"workspace_{workspace_slug.replace('-', '_')}"
