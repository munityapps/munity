import { useDeleteUserMutation, useGetUsersQuery, User } from "./slice";
import moment from 'moment';
import { Column } from 'primereact/column';
import { Button } from "primereact/button";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faTrash } from "@fortawesome/free-solid-svg-icons";
import { faEdit } from '@fortawesome/free-regular-svg-icons';
import MunityDataTable from '../layouts/components/MunityDataTable';
import UserForm from './form';
import { FunctionComponent, useEffect, useState } from "react";
import { useDispatch } from "react-redux";
import { setUserInEdition } from "./slice";
import { confirmPopup } from 'primereact/confirmpopup';
import { addNotification } from "../notifications/slice";
import { ProgressSpinner } from 'primereact/progressspinner';
import { Avatar } from "primereact/avatar";

const UserList: FunctionComponent<{}> = () => {
    const dispatch = useDispatch();
    const [showForm, setShowForm] = useState<boolean>(false);
    const { data: users, error:errorGetUsers, isFetching, isLoading } = useGetUsersQuery();

    const [deleteUser, { isLoading: isDeleting, isError: deleteError, isSuccess: deleteSuccess }] = useDeleteUserMutation();

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

    if (isLoading || isFetching) {
        return <ProgressSpinner />;
    }

    return <>
        <UserForm show={showForm} onClose={() => setShowForm(false)}/>
        <MunityDataTable
            createNew={createNew}
            value={users?.results}
            className="data-table"
            dataKey="id"
            filters={{
                'username': { operator: "and", constraints: [{ value: null, matchMode: "contains" }] },
                'firstname': { operator: "and", constraints: [{ value: null, matchMode: "contains" }] },
                'lastname': { operator: "and", constraints: [{ value: null, matchMode: "contains" }] },
                'email': { operator: "and", constraints: [{ value: null, matchMode: "contains" }] },
                'created': { operator: "and", constraints: [{ value: null, matchMode: "dateIs" }] }
            }}
            filterDisplay="menu"
            globalFilterFields={['username', 'firstname', 'lastname', 'email', 'created']}
            emptyMessage="No users found."
        >
            <Column body={<Avatar icon="pi pi-user" className="p-mr-2" size="large" />} />
            <Column field="username" header="Username" filter filterPlaceholder="Search by username" />
            <Column field="email" header="Email" filter filterPlaceholder="Search by db email" />
            <Column field="first_name" header="Firstname" filter filterPlaceholder="Search by firstname" />
            <Column field="last_name" header="Lastname" filter filterPlaceholder="Search by lastname" />
            <Column field="created" body={user => <div>{moment(new Date(user.created)).fromNow()}</div>} header="Created at" filter filterPlaceholder="Search by date of creation" />
            <Column body={actions} bodyStyle={{ display: 'flex', justifyContent: 'flex-end' }} />
        </MunityDataTable>
    </>;
}

export default UserList;
