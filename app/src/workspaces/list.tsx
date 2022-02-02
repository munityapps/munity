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
import monsterImg from '../assets/logo512.png';
import { useAppSelector } from "../hooks";
import { useGetUsersQuery, User, UserRoleWorkspace } from "../user/slice";
import { getURLForFile } from "../helper";

const WorkspaceList: FunctionComponent<{}> = () => {
    const dispatch = useDispatch();
    const [showForm, setShowForm] = useState<boolean>(false);
    const { data: workspaces, error: errorGetWorkspace, isFetching, isLoading } = useGetWorkspacesQuery();
    const currentUser = useAppSelector(state => state.authentication.currentUser)
    const { data: users } = useGetUsersQuery();

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

        const wsUsers: User[] = users.results.filter((u: User) =>
            u.user_role_workspaces.map(
                (urw: UserRoleWorkspace) => urw.workspace
            ).indexOf(props.workspace.slug) > -1
        ).map((u: User) => {
            return u.avatar && typeof u.avatar !== "string" ?
                <Avatar shape="circle" className="p-mr-2" size="xlarge" image={getURLForFile(u.avatar.file)} /> :
                <Avatar icon="pi pi-user" className="p-mr-1" shape="circle" size="large" />
        })

        const moreUser = wsUsers.length - 5 > 0 ? wsUsers.length - 5 : 0;
        if (wsUsers.length > 5) wsUsers.length = 5;

        return <div className="workspace-card p-shadow-4">
            <div className="illustration">
                {
                    props.workspace.icon && typeof props.workspace.icon !== "string" ?
                        <img alt="icon" src={getURLForFile(props.workspace.icon.file)} /> :
                        <img src={monsterImg} alt="monster" />
                }
                {actions(props.workspace)}
            </div>
            <div className="text">
                <div className="title">
                    {props.workspace.name}
                </div>
                <div className="metric">
                    {props.workspace.slug}
                </div>
                <div className="usedBy">
                    <AvatarGroup className="p-mb-3">
                        {wsUsers}
                        {moreUser > 0 ? <Avatar label={`+${moreUser}`} shape="circle" size="large" style={{ backgroundColor: '#9c27b0', color: '#ffffff' }} /> : null}
                    </AvatarGroup>
                </div>
            </div>
        </div>;
    };

    return <div className="workspace-wrapper">
        <div className="workspace-cards">
            <div className="workspace-title">Liste des projets</div>
            <WorkspaceForm show={showForm} onClose={() => setShowForm(false)} />
            {workspaces?.results.map(w => {
                return <WorkspaceCard key={w.slug} workspace={w} />
            })}
            {currentUser.is_superuser && <Button className="createNew p-button-rounded p-button-lg" icon="pi pi-plus" onClick={createNew} />}
        </div>
    </div>;
}

export default WorkspaceList;
