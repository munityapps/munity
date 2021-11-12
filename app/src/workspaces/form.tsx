import { useUpdateWorkspaceMutation, useCreateWorkspaceMutation, Workspace } from "./slice";
import MunityDialog from '../layouts/components/MunityDialog';
import { FunctionComponent, useEffect, useState } from "react";
import { InputText } from "primereact/inputtext";
import { useDispatch } from "react-redux";
import { useAppSelector } from "../hooks";
import { addNotification } from "../notifications/slice";

const WorkspaceForm: FunctionComponent<{show:boolean, onClose:Function}> = props => {
    const dispatch = useDispatch();
    const [slug, setSlug] = useState<string>("");
    const [dbConnection, setDbConnection] = useState<string>("");
    const { workspaceInEdition } = useAppSelector(state => state.workspace)

    const [createWorkspace, { isLoading: isCreating, isError: createError, isSuccess: createSuccess }] = useCreateWorkspaceMutation();
    const [updateWorkspace, { isLoading: isUpdating, isError: updateError, isSuccess: updateSuccess }] = useUpdateWorkspaceMutation();

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

    useEffect(() => {
        if (workspaceInEdition) {
            setSlug(workspaceInEdition.slug);
            setDbConnection(workspaceInEdition.db_connection);
        } else {
            setSlug('');
            setDbConnection('');
        }
    }, [workspaceInEdition]);

    const saveWorkspace = () => {
        if (!workspaceInEdition) {
            const ws: Workspace = {
                slug,
                db_connection: dbConnection
            }
            createWorkspace(ws);
        } else {
            const ws: Workspace = Object.assign({}, workspaceInEdition);
            ws.slug = slug;
            ws.db_connection = dbConnection;
            updateWorkspace(ws);
        }
    };

    return <>
        <MunityDialog title="Workspace form" visible={props.show} onSave={saveWorkspace} onHide={props.onClose}>
            <div className="p-fluid">
                <div className="p-field p-grid">
                    <label htmlFor="firstname4" className="p-col-12 p-md-2">Slug</label>
                    <div className="p-col-12 p-md-10">
                        <InputText readOnly={workspaceInEdition} id="slug" type="text" value={slug} onChange={(e) => setSlug(e.target.value)} />
                    </div>
                </div>
                <div className="p-field p-grid">
                    <label htmlFor="lastname4" className="p-col-12 p-md-2">DB Connection</label>
                    <div className="p-col-12 p-md-10">
                        <InputText id="db_connection" type="text" value={dbConnection} onChange={(e) => setDbConnection(e.target.value)} />
                    </div>
                </div>
            </div>
        </MunityDialog>
    </>;
}

export default WorkspaceForm ;
