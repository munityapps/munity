import { useDeleteWorkspaceMutation, useGetWorkspacesQuery, Workspace } from "./slice";
import { Button } from "primereact/button";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faDoorOpen, faTrash } from "@fortawesome/free-solid-svg-icons";
import { useHistory } from 'react-router';
import { faEdit } from '@fortawesome/free-regular-svg-icons';
import WorkspaceForm from './form';
import { FunctionComponent, useEffect, useState } from "react";
import { useDispatch } from "react-redux";
import { setWorkspaceInEdition } from "./slice";
import { confirmPopup } from 'primereact/confirmpopup';
import { addNotification } from "../notifications/slice";
import { Avatar } from "primereact/avatar";
import { AvatarGroup } from "primereact/avatargroup";
import monsterImg from '../assets/monster.svg';

const WorkspaceList: FunctionComponent<{}> = () => {
    const dispatch = useDispatch();
    const [showForm, setShowForm] = useState<boolean>(false);
    const { data: workspaces, error: errorGetWorkspace, isFetching, isLoading } = useGetWorkspacesQuery();

    const [deleteWorkspace, { isLoading: isDeleting, isError: deleteError, isSuccess: deleteSuccess }] = useDeleteWorkspaceMutation();

    const router = useHistory();
    // Update alert

    useEffect(() => {
        if (errorGetWorkspace) {
            dispatch(addNotification({
                type: 'error',
                message: 'Cannot get customers'
            }));
        }
    }, [errorGetWorkspace, dispatch]);
    // Delete alert

    useEffect(() => {
        if (deleteError) {
            dispatch(addNotification({
                type: 'error',
                message: 'Cannot delete customer'
            }));
        }
    }, [deleteError, dispatch]);

    useEffect(() => {
        if (deleteSuccess) {
            dispatch(addNotification({
                type: 'success',
                message: 'Customer deleted'
            }));
        }
    }, [deleteSuccess, dispatch]);

    const actions = (w: Workspace) => <div className="action-list">
        <div>
            <Button onClick={() => window.location.href = (`${window.location.protocol}//${window.location.host}/workspace/${w.slug}`)}>
                <FontAwesomeIcon icon={faDoorOpen} />
            </Button>
        </div>
        <div>
            <Button onClick={() => {
                dispatch(setWorkspaceInEdition(w));
                setShowForm(true);
            }}>
                <FontAwesomeIcon icon={faEdit} />
            </Button>
        </div>
        <div>
            <Button onClick={() =>
                confirmPopup({
                    message: 'Are you sure you want to proceed?',
                    icon: 'pi pi-exclamation-triangle',
                    accept: () => deleteWorkspace(w.slug),
                    reject: () => { }
                })}>
                <FontAwesomeIcon icon={faTrash} />
            </Button>
        </div>
    </div >;

    const createNew = () => {
        dispatch(setWorkspaceInEdition(null));
        setShowForm(true);
    }

    const WorkspaceCard: React.FC<{ workspace: Workspace }> = props => {
        return <div className="workspace-card p-shadow-4">
            <div className="illustration">
                <img src={monsterImg} alt="monster"/>
                {actions(props.workspace)}
            </div>
            <div className="text">
                <div className="title">
                    {props.workspace.slug}
                </div>
                <div className="metric">
                    DB Connection: {props.workspace.db_connection}
                </div>
                <div className="usedBy">
                    <AvatarGroup className="p-mb-3">
                        <Avatar icon="pi pi-user" size="large" shape="circle" />
                        <Avatar icon="pi pi-user" size="large" shape="circle" />
                        <Avatar icon="pi pi-user" size="large" shape="circle" />
                        <Avatar icon="pi pi-user" size="large" shape="circle" />
                        <Avatar icon="pi pi-user" size="large" shape="circle" />
                        <Avatar label="+9" shape="circle" size="large" style={{ backgroundColor: '#9c27b0', color: '#ffffff' }} />
                    </AvatarGroup>
                </div>
            </div>
        </div>;
    };

    return <div className="workspace-cards">
        <WorkspaceForm show={showForm} onClose={() => setShowForm(false)} />
        {workspaces?.results.map(w => {
            return <WorkspaceCard workspace={w} />
        })}
        <Button className="createNew p-button-rounded p-button-lg" icon="pi pi-plus" onClick={createNew}/>
    </div>;
}

export default WorkspaceList;
