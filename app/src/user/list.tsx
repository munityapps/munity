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
import { useTranslation } from "react-i18next";

const UserList: FunctionComponent<{}> = () => {
    const dispatch = useDispatch();
    const [showForm, setShowForm] = useState<boolean>(false);
    const { data: users, error:errorGetUsers } = useGetUsersQuery();
    const { data: roles, isFetching:isFetchingRole } = useGetRolesQuery();
    const { t } = useTranslation();

    const [deleteUser, { isError: deleteError, isSuccess: deleteSuccess }] = useDeleteUserMutation();

    useEffect(() => {
        if (errorGetUsers) {
            dispatch(addNotification({
                type: 'error',
                message: t('errors:Cannot get users')
            }));
        }
    }, [errorGetUsers, dispatch]);
    // Delete alert

    useEffect(() => {
        if (deleteError) {
            dispatch(addNotification({
                type: 'error',
                message: t('errors:Cannot delete user')
            }));
        }
    }, [deleteError, dispatch]);

    useEffect(() => {
        if (deleteSuccess) {
            dispatch(addNotification({
                type: 'success',
                message: t('errors:User deleted')
            }));
        }
    }, [deleteSuccess, dispatch]);

    const actions = (u: User) => <div className="action-list">
        <div>
            <Button onClick={() => {
                dispatch(setUserInEdition(u));
                setShowForm(true);
            }}>
                <FontAwesomeIcon icon={faEdit} />&nbsp; {` ${t('common:edit')}`}
            </Button>
        </div>
        <div>
            <Button onClick={() =>
                confirmPopup({
                    message: t('app:are_you_sure'),
                    icon: 'pi pi-exclamation-triangle',
                    accept: () => deleteUser(u.id),
                    reject: () => { }
                })}>
                <FontAwesomeIcon icon={faTrash} />&nbsp; {` ${t('common:delete')}`}
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
            emptyMessage={t('errors:No user found')}
        >
            <Column body={(user:User) =>
                user?.avatar && (typeof user.avatar !== "string") ?
                    <Avatar shape="circle" className="p-mr-2" size="xlarge" image={getURLForFile(user.avatar.file)} /> :
                    <Avatar shape="circle" icon="pi pi-user" className="p-mr-2" size="xlarge" />
            } />
            <Column field="username" header={t('common:username')} filter filterPlaceholder="Search by username" />
            <Column field="email" header={t('common:mail')} filter filterPlaceholder="Search by db email" />
            {/* <Column field="first_name" header="Firstname" filter filterPlaceholder="Search by firstname" />
            <Column field="last_name" header="Lastname" filter filterPlaceholder="Search by lastname" /> */}
            <Column body={(user:User) => user.user_role_workspaces.map(role => {
                return `${role.workspace} (${roles.results.find((r:Role) => r.id === role.role)?.name})`
            }).join(", ")} header={t('common:projects')} />
            <Column field="created" body={user => <div>{moment(new Date(user.created)).fromNow()}</div>} header={t('common:created')} />
            <Column field="is_superuser" header={t('common:is_superuser')} body={user => <div>{user.is_superuser? <FontAwesomeIcon icon={faUserShield}/> : ''}</div>}/>
            <Column field="has_overmind_access" header={t('common:has_overmind_access')} body={user => <div>{user.has_overmind_access ? <FontAwesomeIcon icon={faUserCog}/> : ''}</div>}/>
            <Column body={actions} bodyStyle={{ display: 'flex', justifyContent: 'flex-end' }} />
        </MunityDataTable>
    </>;
}

export default UserList;
