import { useUpdateUserMutation, useCreateUserMutation, User, UserState, UserRoleWorkspace } from "./slice";
import MunityDialog from '../layouts/components/MunityDialog';
import { FunctionComponent, useEffect, useState } from "react";
import { InputText } from "primereact/inputtext";
import { Dropdown } from "primereact/dropdown";
import { useDispatch } from "react-redux";
import { useAppSelector } from "../hooks";
import { addNotification } from "../notifications/slice";
import { useGetWorkspacesQuery } from "../workspaces/slice";
import { Role, useGetRolesQuery } from "../permissions/slice";
import { DataTable } from "primereact/datatable";
import { Column } from "primereact/column";
import { Button } from "primereact/button";
import { Checkbox } from "primereact/checkbox";
import { SelectButton } from "primereact/selectbutton";
import { confirmPopup } from "primereact/confirmpopup";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faBan, faTrash } from "@fortawesome/free-solid-svg-icons";
import { ProgressSpinner } from "primereact/progressspinner";
import { AppState } from "../app/slice";

const UserForm: FunctionComponent<{ show: boolean, onClose: Function }> = props => {
    const dispatch = useDispatch();
    const [firstname, setFirstname] = useState<string>("");
    const [lastname, setLastname] = useState<string>("");
    const [email, setEmail] = useState<string>("");
    const [username, setUsername] = useState<string>("");
    const [userRoleWorkspaces, setUserRoleWorkspaces] = useState<UserRoleWorkspace[]>([]);
    const [isSuperuser, setIsSuperuser] = useState<boolean>(false);
    const { userInEdition } = useAppSelector<UserState>(state => state.user)

    // get workspaces on overmind
    const { data: workspaces, error: errorGetWorkspaces, isFetching: isFetchingWorkspaces, isLoading: isLoadingWorkspaces } = useGetWorkspacesQuery();
    const { data: roles, error: errorGetRoles, isFetching: isFetchingRole, isLoading: isLoadingRole } = useGetRolesQuery();

    const [createUser, { isLoading: isCreating, isError: createError, isSuccess: createSuccess }] = useCreateUserMutation();
    const [updateUser, { isLoading: isUpdating, isError: updateError, isSuccess: updateSuccess }] = useUpdateUserMutation();

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

    useEffect(() => {
        if (userInEdition) {
            setFirstname(userInEdition.first_name);
            setLastname(userInEdition.last_name);
            setUsername(userInEdition.username);
            setEmail(userInEdition.email);
            setIsSuperuser(userInEdition.is_superuser);
            setUserRoleWorkspaces(userInEdition.user_role_workspaces);
        } else {
            setFirstname('');
            setLastname('');
            setUsername('');
            setEmail('');
            setIsSuperuser(false);
            setUserRoleWorkspaces([]);
        }
    }, [userInEdition]);

    const saveUser = () => {
        if (!userInEdition) {
            const user: Partial<User> = {
                first_name: firstname,
                last_name: lastname,
                username,
                is_superuser: isSuperuser,
                // clean emplty rows
                user_role_workspaces: userRoleWorkspaces.filter(ws_role => ws_role.workspace !== '' && ws_role.role !== ''),
                email
            }
            createUser(user);
        } else {
            const user: Partial<User> & Pick<User, "id"> = Object.assign({}, userInEdition);
            user.first_name = firstname;
            user.last_name = lastname;
            user.username = username;
            // clean emplty rows
            user.user_role_workspaces = userRoleWorkspaces.filter(ws_role => ws_role.workspace !== '' && ws_role.role !== '') || [];
            user.is_superuser = isSuperuser;
            user.email = email;
            updateUser(user);
        }
    };

    return <>
        <MunityDialog title="User form" visible={props.show} onSave={saveUser} onHide={props.onClose}>
            <div className="p-fluid">
                <div className="p-field p-grid">
                    <label htmlFor="firstname4" className="p-col-12 p-md-2">Username</label>
                    <div className="p-col-12 p-md-10">
                        <InputText id="username" type="text" value={username} onChange={(e) => setUsername(e.target.value)} />
                    </div>
                </div>
                <div className="p-field p-grid">
                    <label htmlFor="firstname4" className="p-col-12 p-md-2">Firstname</label>
                    <div className="p-col-12 p-md-10">
                        <InputText id="firstname" type="text" value={firstname} onChange={(e) => setFirstname(e.target.value)} />
                    </div>
                </div>
                <div className="p-field p-grid">
                    <label htmlFor="firstname4" className="p-col-12 p-md-2">Lastname</label>
                    <div className="p-col-12 p-md-10">
                        <InputText id="lastname" type="text" value={lastname} onChange={(e) => setLastname(e.target.value)} />
                    </div>
                </div>
                <div className="p-field p-grid">
                    <label htmlFor="firstname4" className="p-col-12 p-md-2">Email</label>
                    <div className="p-col-12 p-md-10">
                        <InputText id="email" type="text" value={email} onChange={(e) => setEmail(e.target.value)} />
                    </div>
                </div>
                <div className="p-field p-grid">
                    <div className="p-col-12 p-md-2">
                        <Checkbox inputId="is_superuser" value={true} onChange={() => setIsSuperuser(!isSuperuser)} checked={isSuperuser} />
                    </div>
                    <label htmlFor="is_superuser" className="p-col-12 p-md-10">Super administrateur</label>
                </div>
            </div>
            {(errorGetWorkspaces === false) ?
                (isFetchingWorkspaces === false && isFetchingRole === false) ?
                    <>
                        <DataTable value={userRoleWorkspaces} responsiveLayout="scroll">
                            <Column body={(role, {rowIndex}) => {
                                return <Dropdown value={role.workspace} options={workspaces?.results.map(w => w.slug)} onChange={e => {
                                    const newUserRoleWorkspace = userRoleWorkspaces.slice(0);
                                    newUserRoleWorkspace[rowIndex].workspace = e.value;
                                    setUserRoleWorkspaces(newUserRoleWorkspace);
                                }} />
                            }} header="Workspace" />
                            <Column body={(role, {rowIndex}) => {
                                console.log(role);
                                return <SelectButton value={role.role} options={roles.results.map((r: Role) => {
                                    return {
                                        name: r.name,
                                        value: r.id
                                    };
                                })} itemTemplate={role => <div key={role.id}>{role.name}</div>} onChange={(e) => {
                                    const newUserRoleWorkspace = userRoleWorkspaces.slice(0);
                                    newUserRoleWorkspace[rowIndex].role = e.value;
                                    setUserRoleWorkspaces(newUserRoleWorkspace);
                                }} />
                            }} header="Role" />
                            <Column body={(role, { rowIndex }) =>
                                <div>
                                    <Button className="pi" onClick={() => {
                                        const newUserRoleWorkspace = userRoleWorkspaces.slice(0);
                                        newUserRoleWorkspace.splice(rowIndex,1);
                                        setUserRoleWorkspaces(newUserRoleWorkspace);
                                    }}>
                                        <FontAwesomeIcon icon={faBan} />
                                    </Button>
                                </div>
                            } />
                        </DataTable>
                        <Button icon="pi pi-plus" label="Add new workspace access" onClick={() => {
                            const newUserRoleWorkspace = userRoleWorkspaces.slice(0);
                            newUserRoleWorkspace.push({
                                workspace: '',
                                role: ''
                            });
                            setUserRoleWorkspaces(newUserRoleWorkspace);
                        }} />
                    </> : <ProgressSpinner />
                : null }
        </MunityDialog>
    </>;
}

export default UserForm;

