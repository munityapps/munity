import { useUpdateUserMutation, useCreateUserMutation, User, UserState} from "./slice";
import MunityDialog from '../layouts/components/MunityDialog';
import { FunctionComponent, useEffect, useState } from "react";
import { InputText } from "primereact/inputtext";
import { useDispatch } from "react-redux";
import { useAppSelector } from "../hooks";
import { addNotification } from "../notifications/slice";
import { Workspace } from "../workspaces/slice";

const UserForm: FunctionComponent<{show:boolean, onClose:Function}> = props => {
    const dispatch = useDispatch();
    const [firstname, setFirstname] = useState<string>("");
    const [lastname, setLastname] = useState<string>("");
    const [email, setEmail] = useState<string>("");
    const [username, setUsername] = useState<string>("");
    const [workspace, setWorkspace] = useState<Workspace|null>(null);
    const { userInEdition } = useAppSelector<UserState>(state => state.user)

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
            setWorkspace(userInEdition.workspace);
        } else {
            setFirstname('');
            setLastname('');
            setUsername('');
            setEmail('');
            setWorkspace(null);
        }
    }, [userInEdition]);

    const saveWorkspace = () => {
        if (!userInEdition) {
            const user: Partial<User> = {
                first_name:firstname,
                last_name:lastname,
                username,
                workspace,
                email
            }
            createUser(user);
        } else {
            const user: Partial<User> & Pick<User, "id"> = Object.assign({}, userInEdition);
            user.first_name = firstname;
            user.last_name = lastname;
            user.username = username;
            user.workspace = workspace;
            user.email = email;
            updateUser(user);
        }
    };

    return <>
        <MunityDialog title="User form" visible={props.show} onSave={saveWorkspace} onHide={props.onClose}>
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
                {/* <div className="p-field p-grid">
                    <label htmlFor="firstname4" className="p-col-12 p-md-2">Workspace</label>
                    <div className="p-col-12 p-md-10">
                        <InputText id="username" type="text" value={username} onChange={(e) => setWorkspace(e.target.value)} />
                    </div>
                </div> */}
            </div>
        </MunityDialog>
    </>;
}

export default UserForm ;

