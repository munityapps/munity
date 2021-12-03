import { useDeleteUserMutation, useGetUsersQuery, User } from "./slice";
import moment from 'moment';
import { Column } from 'primereact/column';
import { Button } from "primereact/button";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faTrash, faUserCog, faUserShield } from "@fortawesome/free-solid-svg-icons";
import { faEdit } from '@fortawesome/free-regular-svg-icons';
import MunityDataTable from '../layouts/components/MunityDataTable';
import UserForm from './form';
import { FunctionComponent, useEffect, useState } from "react";
import { useDispatch } from "react-redux";
import { setUserInEdition } from "./slice";
import { confirmPopup } from 'primereact/confirmpopup';
import { addNotification } from "../notifications/slice";
import { Avatar } from "primereact/avatar";
import { Role, useGetRolesQuery } from "../permissions/slice";
import { ProgressSpinner } from "primereact/progressspinner";
import { getURLForFile } from "../helper";

const UserList: FunctionComponent<{}> = () => {
    const dispatch = useDispatch();
    const [showForm, setShowForm] = useState<boolean>(false);
    const { data: users, error:errorGetUsers } = useGetUsersQuery();
    const { data: roles, isFetching:isFetchingRole } = useGetRolesQuery();

    const [deleteUser, { isError: deleteError, isSuccess: deleteSuccess }] = useDeleteUserMutation();

    useEffect(() => {
        if (errorGetUsers) {
            dispatch(addNotification({
                type: 'error',
                message: 'Cannot get users'
            }));
        }
    }, [errorGetUsers, dispatch]);
    // Delete alert

    useEffect(() => {
        if (deleteError) {
            dispatch(addNotification({
                type: 'error',
                message: 'Cannot delete user'
            }));
        }
    }, [deleteError, dispatch]);

    useEffect(() => {
        if (deleteSuccess) {
            dispatch(addNotification({
                type: 'success',
                message: 'user deleted'
            }));
        }
    }, [deleteSuccess, dispatch]);

    const actions = (u: User) => <div className="action-list">
        <div>
            <Button onClick={() => {
                dispatch(setUserInEdition(u));
                setShowForm(true);
            }}>
                <FontAwesomeIcon icon={faEdit} />&nbsp; {` Edit`}
            </Button>
        </div>
        <div>
            <Button onClick={() =>
                confirmPopup({
                    message: 'Are you sure you want to proceed?',
                    icon: 'pi pi-exclamation-triangle',
                    accept: () => deleteUser(u.id),
                    reject: () => { }
                })}>
                <FontAwesomeIcon icon={faTrash} />&nbsp; {` Delete `}
            </Button>
        </div>
    </div >;

    const createNew = () => {
        dispatch(setUserInEdition(null));
        setShowForm(true);
    }

    if (isFetchingRole || isFetchingRole) {
        return <ProgressSpinner className="data-table-spinner" />;
    }

    return <>
        <UserForm show={showForm} onClose={() => {
            setShowForm(false);
            dispatch(setUserInEdition(null));
        }}/>
        <MunityDataTable
            createNew={createNew}
            value={users?.results}
            className="data-table"
            dataKey="id"
            filters={{
                'username': { operator: "and", constraints: [{ value: null, matchMode: "contains" }] },
                // 'firstname': { operator: "and", constraints: [{ value: null, matchMode: "contains" }] },
                // 'lastname': { operator: "and", constraints: [{ value: null, matchMode: "contains" }] },
                'email': { operator: "and", constraints: [{ value: null, matchMode: "contains" }] },
                'created': { operator: "and", constraints: [{ value: null, matchMode: "dateIs" }] }
            }}
            filterDisplay="menu"
            globalFilterFields={['username', /**'firstname', 'lastname', **/'email', 'created']}
            emptyMessage="Aucun utilisteur trouvé."
        >
            <Column body={(user:User) =>
                user?.avatar && (typeof user.avatar !== "string") ?
                    <Avatar className="p-mr-2" size="xlarge" image={getURLForFile(user.avatar.file)} /> :
                    <Avatar icon="pi pi-user" className="p-mr-2" size="xlarge" />
            } />
            <Column field="username" header="Identifiant" filter filterPlaceholder="Rechercher par identifiant" />
            <Column field="email" header="Email" filter filterPlaceholder="Search by db email" />
            {/* <Column field="first_name" header="Firstname" filter filterPlaceholder="Search by firstname" />
            <Column field="last_name" header="Lastname" filter filterPlaceholder="Search by lastname" /> */}
            <Column body={(user:User) => user.user_role_workspaces.map(role => {
                return `${role.workspace} (${roles.results.find((r:Role) => r.id === role.role)?.name})`
            }).join(", ")} header="Projets" />
            <Column field="created" body={user => <div>{moment(new Date(user.created)).fromNow()}</div>} header="Créé" />
            <Column field="is_superuser" header="Administrateur" body={user => <div>{user.is_superuser? <FontAwesomeIcon icon={faUserShield}/> : ''}</div>}/>
            <Column field="has_overmind_access" header="Gestionnaire" body={user => <div>{user.has_overmind_access ? <FontAwesomeIcon icon={faUserCog}/> : ''}</div>}/>
            <Column body={actions} bodyStyle={{ display: 'flex', justifyContent: 'flex-end' }} />
        </MunityDataTable>
    </>;
}

export default UserList;
