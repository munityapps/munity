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
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faBan } from "@fortawesome/free-solid-svg-icons";
import { ProgressSpinner } from "primereact/progressspinner";
import { Avatar } from "primereact/avatar";
import { FileUploadUploadParams } from 'primereact/fileupload';
import SimpleUploader from '../files/SimpleUploader';
import { File } from '../files/slice';
import { getURLForFile } from "../helper";
import { useTranslation } from "react-i18next";

const UserForm: FunctionComponent<{ show: boolean, onClose: Function }> = props => {
    const dispatch = useDispatch();
    const [firstname, setFirstname] = useState<string>("");
    const [lastname, setLastname] = useState<string>("");
    const [phone, setPhone] = useState<string>("");
    const [email, setEmail] = useState<string>("");
    const [errorField, setErrorField] = useState<string[]>([]);
    const [username, setUsername] = useState<string>("");
    const [newPassword, setNewPassword] = useState<string>("");
    const [confirmPassword, setConfirmPassword] = useState<string>("");
    const [uploadedAvatar, setUploadedAvatar] = useState<File | undefined>(undefined);
    const [userRoleWorkspaces, setUserRoleWorkspaces] = useState<UserRoleWorkspace[]>([]);
    const [isSuperuser, setIsSuperuser] = useState<boolean>(false);
    const [hasOvermindAccess, setHasOvermindAccess] = useState<boolean>(false);
    const { userInEdition } = useAppSelector<UserState>(state => state.user)
    const currentUser = useAppSelector(state => state.authentication.currentUser)
    const { t } = useTranslation()

    // get workspaces on overmind
    const { data: workspaces } = useGetWorkspacesQuery();
    const { data: roles } = useGetRolesQuery();

    const [createUser, { isError: createError, isSuccess: createSuccess }] = useCreateUserMutation();
    const [updateUser, { isError: updateError, isSuccess: updateSuccess }] = useUpdateUserMutation();

    useEffect(() => {
        if (updateError) {
            dispatch(addNotification({
                type: 'error',
                message: t('error:Cannot update user')
            }));
        }
    }, [updateError, dispatch]);

    useEffect(() => {
        if (updateSuccess) {
            dispatch(addNotification({
                type: 'success',
                message: t('error:User updated')
            }));
        }
    }, [updateSuccess, dispatch]);

    // Create alert
    useEffect(() => {
        if (createSuccess) {
            dispatch(addNotification({
                type: 'success',
                message: t('error:User created')
            }));
        }
    }, [createSuccess, dispatch]);

    useEffect(() => {
        if (createError) {
            dispatch(addNotification({
                type: 'error',
                message: t('error:Cannot create user')
            }));
        }
    }, [createError, dispatch]);

    useEffect(() => {
        if (userInEdition) {
            setErrorField([]);
            setFirstname(userInEdition.first_name);
            setLastname(userInEdition.last_name);
            setUsername(userInEdition.username);
            setEmail(userInEdition.email);
            setPhone(userInEdition.phone_number || '');
            setIsSuperuser(userInEdition.is_superuser);
            setHasOvermindAccess(userInEdition.has_overmind_access);
            setUserRoleWorkspaces(userInEdition.user_role_workspaces);
            setUploadedAvatar(undefined);
        } else {
            setErrorField([]);
            setFirstname('');
            setLastname('');
            setUsername('');
            setEmail('');
            setPhone('');
            setIsSuperuser(false);
            setHasOvermindAccess(false);
            setUploadedAvatar(undefined);
            setUserRoleWorkspaces([{
                workspace: '',
                role: ''
            }]);
        }
    }, [userInEdition, props.show]);

    useEffect(() => {
        const newUserRoleWorkspaces = userRoleWorkspaces.slice(0);
        if (newUserRoleWorkspaces.length > 0) {
            const lastUserRoleWorkspace = newUserRoleWorkspaces[newUserRoleWorkspaces.length - 1];
            if (lastUserRoleWorkspace.workspace !== '' && lastUserRoleWorkspace.role !== '') {
                newUserRoleWorkspaces.push({
                    workspace: '',
                    role: ''
                });
                setUserRoleWorkspaces(newUserRoleWorkspaces);
            }
        } else {
            setUserRoleWorkspaces([{
                workspace: '',
                role: ''
            }])
        }
    }, [userRoleWorkspaces])

    const saveUser = () => {
        const error = [];
        if (username.length === 0) {
            error.push('username');
            dispatch(addNotification({
                type: 'error',
                message: "Username required"
            }))
        }
        if (newPassword.length > 0 && newPassword !== confirmPassword) {
            error.push('password');
            dispatch(addNotification({
                type: 'error',
                message: "Password are different"
            }))
        }
        if (error.length > 0) {
            setErrorField(error);
            return false;
        }
        if (!userInEdition) {
            const user: Partial<User> = {
                first_name: firstname,
                last_name: lastname,
                phone_number: phone,
                username,
                is_superuser: isSuperuser,
                has_overmind_access: hasOvermindAccess,
                user_role_workspaces: userRoleWorkspaces.filter(ws_role => ws_role.workspace !== '' && ws_role.role !== ''),
                email,
                password: newPassword.length > 0 ? newPassword : undefined,
            }
            // add fresh uploaded avatar or do not send JSON transcryption
            createUser(user);
        } else {
            const user: Partial<User> = Object.assign({}, userInEdition);
            user.first_name = firstname;
            user.last_name = lastname;
            user.username = username;
            user.phone_number= phone;
            user.user_role_workspaces = userRoleWorkspaces.filter(ws_role => ws_role.workspace !== '' && ws_role.role !== '') || [];
            user.is_superuser = isSuperuser;
            user.has_overmind_access = hasOvermindAccess;
            user.avatar = uploadedAvatar?.id;
            user.email = email;
            user.password = newPassword.length > 0 ? newPassword : undefined;
            updateUser(user);
        }
        return true;
    };

    return <>
        <MunityDialog title={t('app:user_form')} visible={props.show} onSave={saveUser} onHide={props.onClose}>
            <div className="p-d-flex p-jc-center p-m-2">
                {
                    uploadedAvatar ?
                        <Avatar shape="circle" className="p-mr-2" size="xlarge" image={uploadedAvatar.file} /> :
                        userInEdition?.avatar && (typeof userInEdition.avatar !== "string") ?
                            <Avatar shape="circle" className="p-mr-2" size="xlarge" image={getURLForFile(userInEdition.avatar.file)} /> :
                            <Avatar shape="circle" icon="pi pi-user" className="p-mr-2" size="xlarge" />
                }
                <SimpleUploader
                    onUpload={(e: FileUploadUploadParams) => {
                        setUploadedAvatar(JSON.parse(e.xhr.response));
                    }}
                    label={t('app:change_avatar')}
                    auto
                    accept="image/*"
                />
            </div>
            <div className="p-fluid">
                <div className="p-field p-grid">
                    <label htmlFor="firstname4" className="p-col-12 p-md-2">{t('common:username')}</label>
                    <div className="p-col-12 p-md-10">
                        <InputText id="username" className={errorField.includes('username') ? 'p-invalid' : ''} type="text" value={username} onChange={(e) => setUsername(e.target.value)} />
                    </div>
                </div>
                <div className="p-field p-grid">
                    <label htmlFor="firstname4" className="p-col-12 p-md-2">{t('common:firstname')}</label>
                    <div className="p-col-12 p-md-10">
                        <InputText id="firstname" type="text" value={firstname} onChange={(e) => setFirstname(e.target.value)} />
                    </div>
                </div>
                <div className="p-field p-grid">
                    <label htmlFor="firstname4" className="p-col-12 p-md-2">{t('common:lastname')}</label>
                    <div className="p-col-12 p-md-10">
                        <InputText id="lastname" type="text" value={lastname} onChange={(e) => setLastname(e.target.value)} />
                    </div>
                </div>
                <div className="p-field p-grid">
                    <label htmlFor="firstname4" className="p-col-12 p-md-2">{t('common:mail')}</label>
                    <div className="p-col-12 p-md-10">
                        <InputText id="email" type="text" value={email} onChange={(e) => setEmail(e.target.value)} />
                    </div>
                </div>
                <div className="p-field p-grid">
                    <label htmlFor="phone" className="p-col-12 p-md-2">{t('common:phone')}</label>
                    <div className="p-col-12 p-md-10">
                        <InputText id="phone" type="text" value={phone} onChange={(e) => setPhone(e.target.value)} />
                    </div>
                </div>
                <div className="p-field p-grid">
                    <label htmlFor="password" className="p-col-12 p-md-2">{t('common:password')}</label>
                    <div className="p-col-12 p-md-10">
                        <InputText id="password" className={errorField.includes('password') ? 'p-invalid' : ''} type="password" value={newPassword} onChange={(e) => setNewPassword(e.target.value)} />
                    </div>
                </div>
                <div className="p-field p-grid">
                    <label htmlFor="confirm_password" className="p-col-12 p-md-2">{t('common:confirm_password')}</label>
                    <div className="p-col-12 p-md-10">
                        <InputText id="confirm_password" className={errorField.includes('password') ? 'p-invalid' : ''} type="password" value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} />
                    </div>
                </div>
                {
                    currentUser.is_superuser &&
                    <div className="p-field p-grid">
                        <div className="p-col-12 p-md-2">
                            <Checkbox inputId="is_superuser" value={true} onChange={() => setIsSuperuser(!isSuperuser)} checked={isSuperuser} />
                        </div>
                        <label htmlFor="is_superuser" className="p-col-12 p-md-10">{t('common:is_superuser')}</label>
                    </div>
                }
                <div className="p-field p-grid">
                    <div className="p-col-12 p-md-2">
                        <Checkbox inputId="has_overmind_access" value={true} onChange={() => setHasOvermindAccess(!hasOvermindAccess)} checked={hasOvermindAccess} />
                    </div>
                    <label htmlFor="has_overmind_access" className="p-col-12 p-md-10">{t('common:has_overmind_access')}</label>
                </div>
            </div>
            {
                (workspaces && roles) ?
                    <>
                        <DataTable value={userRoleWorkspaces} responsiveLayout="scroll">
                            <Column body={(role, { rowIndex }) => {
                                return <Dropdown value={role.workspace} options={workspaces?.results.filter(w => {
                                    // @TODO do not show already set workspaces
                                    return true;
                                }).map(w => w.slug)} onChange={e => {
                                    let newUserRoleWorkspaces = userRoleWorkspaces.slice(0);
                                    let newUserRoleWorkspace = Object.assign({}, newUserRoleWorkspaces[rowIndex]);
                                    newUserRoleWorkspace.workspace = e.value;
                                    newUserRoleWorkspaces[rowIndex] = newUserRoleWorkspace;
                                    setUserRoleWorkspaces(newUserRoleWorkspaces);
                                }} />
                            }} header="Projet" />
                            <Column body={(role, { rowIndex }) => {
                                return <SelectButton value={role.role} options={roles.results.map((r: Role) => {
                                    return {
                                        name: r.name,
                                        value: r.id
                                    };
                                })} itemTemplate={role => <div key={role.id}>{role.name}</div>} onChange={(e) => {
                                    let newUserRoleWorkspaces = userRoleWorkspaces.slice(0);
                                    let newUserRoleWorkspace = Object.assign({}, newUserRoleWorkspaces[rowIndex]);
                                    newUserRoleWorkspace.role = e.value;
                                    newUserRoleWorkspaces[rowIndex] = newUserRoleWorkspace;
                                    setUserRoleWorkspaces(newUserRoleWorkspaces);
                                }} />
                            }} header="Type de compte" />
                            <Column body={(role, { rowIndex }) => {
                                if (role.role === '' || role.workspace === '') return null
                                return <div>
                                    <Button className="pi" onClick={() => {
                                        let newUserRoleWorkspace = userRoleWorkspaces.slice(0);
                                        newUserRoleWorkspace.splice(rowIndex, 1);
                                        setUserRoleWorkspaces(newUserRoleWorkspace);
                                    }}>
                                        <FontAwesomeIcon icon={faBan} />
                                    </Button>
                                </div>
                            }} />
                        </DataTable>
                    </> : <ProgressSpinner />
            }
        </MunityDialog>
    </>;
}

export default UserForm;

