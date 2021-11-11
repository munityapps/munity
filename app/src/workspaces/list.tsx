import { useCreateWorkspaceMutation, useDeleteWorkspaceMutation, useGetWorkspacesQuery, useUpdateWorkspaceMutation, Workspace } from "./slice";
import { Column } from 'primereact/column';
import { Button } from "primereact/button";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faDoorOpen, faTrash } from "@fortawesome/free-solid-svg-icons";
import { useHistory } from 'react-router';
import { faEdit } from '@fortawesome/free-regular-svg-icons';
import MunityDataTable from '../layouts/components/MunityDataTable';
import MunityDialog from '../layouts/components/MunityDialog';
import { FunctionComponent, useEffect, useState } from "react";
import { InputText } from "primereact/inputtext";
import { useDispatch } from "react-redux";
import { setWorkspaceInEdition } from "./slice";
import { useAppSelector } from "../hooks";
import { confirmDialog } from 'primereact/confirmdialog';
import { addNotification } from "../notifications/slice";
import { ProgressSpinner } from 'primereact/progressspinner';

const WorkspaceList: FunctionComponent<{}> = () => {
    const dispatch = useDispatch();
    const [showForm, setShowForm] = useState<boolean>(false);
    const [slug, setSlug] = useState<string>("");
    const [dbConnection, setDbConnection] = useState<string>("");
    const { workspaceInEdition } = useAppSelector(state => state.workspace)
    const { data: workspaces, error:errorGetWorkspace, isFetching, isLoading } = useGetWorkspacesQuery();

    const [createWorkspace, { isLoading: isCreating, isError: createError, isSuccess: createSuccess }] = useCreateWorkspaceMutation();
    const [updateWorkspace, { isLoading: isUpdating, isError: updateError, isSuccess: updateSuccess }] = useUpdateWorkspaceMutation();
    const [deleteWorkspace, { isLoading: isDeleting, isError: deleteError, isSuccess: deleteSuccess }] = useDeleteWorkspaceMutation();

    const router = useHistory();
    // Update alert

    useEffect(() => {
        if (errorGetWorkspace) {
            dispatch(addNotification({
                type: 'error',
                message: 'Cannot get workspaces'
            }));
        }
    }, [errorGetWorkspace, dispatch]);

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

    useEffect(() => {
        if (workspaceInEdition) {
            setSlug(workspaceInEdition.slug);
            setDbConnection(workspaceInEdition.db_connection);
        } else {
            setSlug('');
            setDbConnection('');
        }
    }, [workspaceInEdition, showForm]);

    const actions = (w: Workspace) => <div className="action-list">
        <div>
            <Button onClick={() => router.push(`/workspace/${w.slug}`)}>
                <FontAwesomeIcon icon={faDoorOpen} />&nbsp;{`Go to ${w.slug}`}
            </Button>
        </div>
        <div>
            <Button onClick={() => {
                dispatch(setWorkspaceInEdition(w));
                setShowForm(true);
            }}>
                <FontAwesomeIcon icon={faEdit} />&nbsp; {` Edit`}
            </Button>
        </div>
        <div>
            <Button onClick={() =>
                confirmDialog({
                    message: 'Are you sure you want to proceed?',
                    header: 'Confirmation',
                    icon: 'pi pi-exclamation-triangle',
                    accept: () => deleteWorkspace(w.slug),
                    reject: () => { }
                })}>
                <FontAwesomeIcon icon={faTrash} />&nbsp; {` Delete `}
            </Button>
        </div>
    </div >;

    const createNew = () => {
        dispatch(setWorkspaceInEdition(null));
        setShowForm(true);
    }

    if (isLoading || isFetching) {
        return <ProgressSpinner />;
    }

    return <>
        <MunityDialog visible={showForm} onSave={saveWorkspace} onHide={() => setShowForm(false)}>
            <div className="p-fluid">
                <div className="p-field p-grid">
                    <label htmlFor="firstname4" className="p-col-12 p-md-2">Slug</label>
                    <div className="p-col-12 p-md-10">
                        <InputText id="slug" type="text" value={slug} onChange={(e) => setSlug(e.target.value)} />
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
        <MunityDataTable
            createNew={createNew}
            value={workspaces?.results}
            className="workspace-list"
            dataKey="slug"
            filters={{
                'slug': { operator: "and", constraints: [{ value: null, matchMode: "contains" }] },
                'db_connection': { operator: "and", constraints: [{ value: null, matchMode: "contains" }] }
            }}
            filterDisplay="menu"
            globalFilterFields={['slug', 'db_connection']}
            emptyMessage="No workspces found."
        >
            <Column field="slug" header="Slug" filter filterPlaceholder="Search by slug" />
            <Column field="db_connection" header="DBConnection" filter filterPlaceholder="Search by db connection" />
            <Column field="actions" body={actions} bodyStyle={{ display: 'flex', justifyContent: 'flex-end' }} />
        </MunityDataTable>
    </>;
}

export default WorkspaceList;
