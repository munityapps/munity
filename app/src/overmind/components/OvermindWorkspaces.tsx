import { useState } from 'react';
import { useDeleteWorkspaceMutation, useGetWorkspacesQuery } from "../../workspaces/slice";
import { Workspace } from '../../workspaces/slice';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import { Button } from "primereact/button";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faDoorOpen, faTrash } from "@fortawesome/free-solid-svg-icons";
import { WorkspaceForm } from "../../workspaces/form";
import { useHistory } from 'react-router';
import { faEdit } from '@fortawesome/free-regular-svg-icons';
import LayoutDispatcher from '../../layouts/LayoutDispatcher';
import WorkspaceList from '../../workspaces/list';

const OvermindWorkspaces = ()  => {
    const { data: workspaces, error, isFetching, isLoading } = useGetWorkspacesQuery();
    const [deleteWorkspace, { isLoading: isDeleting, isError: deleteError, isSuccess: deleteSuccess }] = useDeleteWorkspaceMutation();
    const [editWorkspace, setEditWorkspace] = useState<Workspace | null>(null);
    const router = useHistory();

    const actions = (w: Workspace) =><>
        <Button onClick={() => router.push(`/workspace/${w.slug}`)}>
            <FontAwesomeIcon icon={faDoorOpen}/>
        </Button>
        <Button onClick={() => setEditWorkspace(w)}>
            <FontAwesomeIcon icon={faEdit}/>
        </Button>
        <Button onClick={() => deleteWorkspace(w.slug)}>
            <FontAwesomeIcon icon={faTrash}/>
        </Button>
        </>;

    // return <div className="p-m-4">
    //     {
    //     }
    //     <WorkspaceForm setEditWorkspace={setEditWorkspace} workspace={editWorkspace} />
    // </div>;
    return <LayoutDispatcher
        layoutName="TwoColumns"
        mainSlot={<WorkspaceForm workspace={editWorkspace} />}
        rightPanelSlot={<WorkspaceList setEditWorkspace={setEditWorkspace}/>}
    />
}

export default OvermindWorkspaces;