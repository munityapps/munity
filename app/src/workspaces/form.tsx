import { useState, useEffect } from "react";
import { InputText } from "primereact/inputtext";
import { Fieldset } from "primereact/fieldset";
import { useCreateWorkspaceMutation, useGetWorkspacesQuery, useDeleteWorkspaceMutation, Workspace, useUpdateWorkspaceMutation } from "./slice";
import { addNotification } from "../notifications/slice";
import { useAppDispatch } from "../hooks";
import { Button } from "primereact/button";

const initialWorkspaceState = {
    slug: "",
    db_connection: "",
};

export const WorkspaceForm = (props: { workspace: Workspace | null }) => {
    const dispatch = useAppDispatch();

    const [workspace, setWorkspace] = useState<Pick<Workspace, 'slug' | 'db_connection'>>(initialWorkspaceState);
    const { isFetching: loadingWorkspace } = useGetWorkspacesQuery();
    const [createWorkspace, { isLoading: isCreating, isError: createError, isSuccess: createSuccess }] = useCreateWorkspaceMutation();
    const [updateWorkspace, { isLoading: isUpdating, isError: updateError, isSuccess: updateSuccess }] = useUpdateWorkspaceMutation();
    const [deleteWorkspace, { isLoading: isDeleting, isError: deleteError, isSuccess: deleteSuccess }] = useDeleteWorkspaceMutation();

    const handleChange = ({ target }: React.ChangeEvent<HTMLInputElement>) => {
        setWorkspace((prev) => ({
            ...prev,
            [target.id]: target.value,
        }));
    }

    let action = "";
    if (loadingWorkspace) {
        action = "Loading workspaces";
    }

    if (isCreating) {
        action = "Creating workspaces";
    }

    if (isUpdating) {
        action = "Updating workspaces";
    }

    if (isDeleting) {
        action = "Deleting workspaces";
    }

    useEffect(() => {
        setWorkspace(props.workspace || initialWorkspaceState);
    }, [props.workspace])

    // Update alert
    useEffect(() => {
        if (updateError) {
            dispatch(addNotification({
                type: 'error',
                message: 'Cannot update workspace'
            }));
        }
    }, [updateError, dispatch]);

    useEffect(() => {
        if (updateSuccess) {
            dispatch(addNotification({
                type: 'success',
                message: 'Workspace updated'
            }));
        }
    }, [updateSuccess, dispatch]);

    // Delete alert
    useEffect(() => {
        if (deleteError) {
            dispatch(addNotification({
                type: 'error',
                message: 'Cannot delete workspace'
            }));
        }
    }, [deleteError, dispatch]);

    useEffect(() => {
        if (deleteSuccess) {
            dispatch(addNotification({
                type: 'success',
                message: 'Workspace deleted'
            }));
            setWorkspace(initialWorkspaceState);
        }
    }, [deleteSuccess, dispatch]);

    // Create alert
    useEffect(() => {
        if (createSuccess) {
            dispatch(addNotification({
                type: 'success',
                message: 'Workspace created'
            }));
        }
    }, [createSuccess, dispatch]);

    useEffect(() => {
        if (createError) {
            dispatch(addNotification({
                type: 'error',
                message: 'Cannot create workspace'
            }));
        }
    }, [createError, dispatch]);


    return <div className="p-grid p-m-4 p-jc-between p-flex-row">
        <Fieldset legend={props.workspace ? `Editing workspace ${props.workspace.slug}` : 'Creating workspace'}>
            <div className="p-shadow-4 p-p-4 p-mb-4">Debug action: {action}</div>
            <div className="p-formgrid p-grid">
                <div className="p-field p-col-12 p-md-6">
                    <label htmlFor="slug">Slug</label>
                    <InputText id="slug" onChange={handleChange} value={workspace.slug} /><br />
                </div>
                <div className="p-field p-col-12 p-md-6">
                    <label htmlFor="db_connection">DB Connection</label>
                    <InputText id="db_connection" onChange={handleChange} value={workspace.db_connection} /><br />
                </div>
            </div>
            <Button onClick={() => props.workspace ? updateWorkspace(workspace) : createWorkspace(workspace)} >{props.workspace ? `Edit ${props.workspace.slug}` : 'Create workspace'} </Button>
            {props.workspace && <Button onClick={() => deleteWorkspace(workspace.slug)} >Delete workspace </Button>}
        </Fieldset>
    </div>;
}

