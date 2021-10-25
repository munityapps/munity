import { useState, useEffect } from "react";
import { InputText } from "primereact/inputtext";
import { Fieldset } from "primereact/fieldset";
import { useCreateUserMutation, useGetUsersQuery, useDeleteUserMutation, User, useUpdateUserMutation } from "./slice";
import { addNotification } from "../notifications/slice";
import { useAppDispatch } from "../../hooks";
import { Button } from "primereact/button";

const initialUserState = {
    id: "",
    username: "",
    first_name: "",
    last_name: "",
    email: "",
    generic_groups: [],
    roles: []
};

export const UserForm = (props: { user: User | null }) => {
    const dispatch = useAppDispatch();

    const [user, setUser] = useState<Pick<User, 'id' | 'username' | 'first_name' | 'last_name' | 'email' | 'roles' | 'generic_groups'>>(initialUserState);
    const { isFetching: loadingUser } = useGetUsersQuery();
    const [createUser, { isLoading: isCreating, isError: createError, isSuccess: createSuccess }] = useCreateUserMutation();
    const [updateUser, { isLoading: isUpdating, isError: updateError, isSuccess: updateSuccess }] = useUpdateUserMutation();
    const [deleteUser, { isLoading: isDeleting, isError: deleteError, isSuccess: deleteSuccess }] = useDeleteUserMutation();

    const handleChange = ({ target }: React.ChangeEvent<HTMLInputElement>) => {
        setUser((prev) => ({
            ...prev,
            [target.id]: target.value,
        }));
    }

    let action = "";
    if (loadingUser) {
        action = "Loading users";
    }

    if (isCreating) {
        action = "Creating users";
    }

    if (isUpdating) {
        action = "Updating users";
    }

    if (isDeleting) {
        action = "Deleting users";
    }

    useEffect(() => {
        setUser(props.user || initialUserState);
    }, [props.user])

    // Update alert
    useEffect(() => {
        if (updateError) {
            dispatch(addNotification({
                type: 'error',
                message: 'Cannot update user'
            }));
        }
    }, [updateError, dispatch]);

    useEffect(() => {
        if (updateSuccess) {
            dispatch(addNotification({
                type: 'success',
                message: 'User updated'
            }));
        }
    }, [updateSuccess, dispatch]);

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
                message: 'User deleted'
            }));
            setUser(initialUserState);
        }
    }, [deleteSuccess, dispatch]);

    // Create alert
    useEffect(() => {
        if (createSuccess) {
            dispatch(addNotification({
                type: 'success',
                message: 'User created'
            }));
        }
    }, [createSuccess, dispatch]);

    useEffect(() => {
        if (createError) {
            dispatch(addNotification({
                type: 'error',
                message: 'Cannot create user'
            }));
        }
    }, [createError, dispatch]);


    return <div className="p-grid p-m-4 p-jc-between p-flex-row">
        <Fieldset legend={props.user ? `Editing user ${props.user.username}` : 'Creating user'}>
            <div className="p-shadow-4 p-p-4 p-mb-4">Debug action: {action}</div>
            <div className="p-formgrid p-grid">
                <div className="p-field p-col-12 p-md-6">
                    <label htmlFor="username">Username</label>
                    <InputText id="username" onChange={handleChange} value={user.username} /><br />
                </div>
                <div className="p-field p-col-12 p-md-6">
                    <label htmlFor="first_name">Firstname</label>
                    <InputText id="first_name" onChange={handleChange} value={user.first_name} /><br />
                </div>
                <div className="p-field p-col-12 p-md-6">
                    <label htmlFor="first_name">Lastname</label>
                    <InputText id="last_name" onChange={handleChange} value={user.last_name} /><br />
                </div>
                <div className="p-field p-col-12 p-md-6">
                    <label htmlFor="email">Email</label>
                    <InputText id="email" onChange={handleChange} value={user.email} /><br />
                </div>
                <div className="p-field p-col-12 p-md-6">
                    <label htmlFor="email">Groups</label>
                    <InputText id="generic_groups" onChange={handleChange} value={user.generic_groups} /><br />
                </div>
                <div className="p-field p-col-12 p-md-6">
                    <label htmlFor="email">Roles</label>
                    <InputText id="roles" value={user.roles} /><br />
                </div>
            </div>
            <Button onClick={() => props.user ? updateUser(user) : createUser(user)} >{props.user ? `Edit ${props.user.username}` : 'Create user'} </Button>
            {props.user && <Button onClick={() => deleteUser(user.id)} >Delete user </Button>}
        </Fieldset>
    </div>;
}
