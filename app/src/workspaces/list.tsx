import { useDeleteWorkspaceMutation, useGetWorkspacesQuery, Workspace } from "./slice";
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import { Button } from "primereact/button";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faDoorOpen, faTrash } from "@fortawesome/free-solid-svg-icons";
import { useHistory } from 'react-router';
import { faEdit } from '@fortawesome/free-regular-svg-icons';

const WorkspaceList = (props:{setEditWorkspace:Function})  => {
    const { data: workspaces, error, isFetching, isLoading } = useGetWorkspacesQuery();
    const [deleteWorkspace, { isLoading: isDeleting, isError: deleteError, isSuccess: deleteSuccess }] = useDeleteWorkspaceMutation();
    const router = useHistory();

    const actions = (w: Workspace) =><>
        <Button onClick={() => router.push(`/workspace/${w.slug}`)}>
            <FontAwesomeIcon icon={faDoorOpen}/>
        </Button>
        <Button onClick={() => props.setEditWorkspace(w)}>
            <FontAwesomeIcon icon={faEdit}/>
        </Button>
        <Button onClick={() => deleteWorkspace(w.slug)}>
            <FontAwesomeIcon icon={faTrash}/>
        </Button>
        </>;

    return <div className="p-m-4">
        {
            <DataTable value={workspaces?.results}>
                <Column field="slug" header="Slug"></Column>
                <Column field="db_connection" header="DBConnection"></Column>
                <Column body={actions} headerStyle={{ width: '8em', textAlign: 'center' }} bodyStyle={{ textAlign: 'center', overflow: 'visible' }} />
            </DataTable>
        }
    </div>;
}

export default WorkspaceList;
