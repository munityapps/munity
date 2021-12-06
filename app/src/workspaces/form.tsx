import { useUpdateWorkspaceMutation, useCreateWorkspaceMutation, Workspace } from "./slice";
import MunityDialog from '../layouts/components/MunityDialog';
import { FunctionComponent, useEffect, useState } from "react";
import { InputText } from "primereact/inputtext";
import { useDispatch } from "react-redux";
import { useAppSelector } from "../hooks";
import { addNotification } from "../notifications/slice";
import slugify from 'slugify';

const WorkspaceForm: FunctionComponent<{ show: boolean, onClose: Function }> = props => {
    const dispatch = useDispatch();
    const [slug, setSlug] = useState<string>("");
    const [name, setName] = useState<string>("");
    const [errors, setErrors] = useState<Array<string>>([]);
    const [dbConnection, setDbConnection] = useState<string>("");
    const { workspaceInEdition } = useAppSelector(state => state.workspace)
    const [slugHasBeenSetByUser, setSlugHasBeenSetByUser] = useState<Boolean>(false);

    const [createWorkspace, { isLoading: isCreating, isError: createError, isSuccess: createSuccess }] = useCreateWorkspaceMutation();
    const [updateWorkspace, { isLoading: isUpdating, isError: updateError, isSuccess: updateSuccess }] = useUpdateWorkspaceMutation();

    useEffect(() => {
        if(!slugHasBeenSetByUser) {
            setSlug(slugify(name, {
                lower:true
            }));
        }
    }, [name, slugHasBeenSetByUser]);

    useEffect(() => {
        if (updateError) {
            dispatch(addNotification({
                type: 'error',
                message: 'Cannot update workspace'
            }));
        }
    }, [updateError, dispatch]);

    useEffect(() => {
        if (updateSuccess) {
            dispatch(addNotification({
                type: 'success',
                message: 'Workspace updated'
            }));
        }
    }, [updateSuccess, dispatch]);

    // Create alert
    useEffect(() => {
        if (createSuccess) {
            dispatch(addNotification({
                type: 'success',
                message: 'Workspace created'
            }));
        }
    }, [createSuccess, dispatch]);

    useEffect(() => {
        if (createError) {
            dispatch(addNotification({
                type: 'error',
                message: 'Cannot create workspace'
            }));
        }
    }, [createError, dispatch]);

    useEffect(() => {
        if (workspaceInEdition) {
            setName(workspaceInEdition.name);
            setSlug(workspaceInEdition.slug);
            setDbConnection(workspaceInEdition.db_connection);
            setSlugHasBeenSetByUser(true);
        } else {
            setSlugHasBeenSetByUser(false);
            setName('');
            setSlug('');
            setDbConnection('');
        }
    }, [workspaceInEdition, props.show]);

    const saveWorkspace = () => {
        setErrors([]);
        const errors: Array<string> = [];
        if (name.length === 0) {
            errors.push('name');
        }
        if (slug.length === 0) {
            errors.push('slug');
        }
        if (errors.length > 0) {
            setErrors(errors);
            dispatch(addNotification({
                type: 'error',
                message: 'Des champs requis sont manquant'
            }));
            return;
        }
        if (!workspaceInEdition) {
            const ws: Workspace = {
                name,
                slug,
                db_connection: dbConnection
            }
            createWorkspace(ws);
        } else {
            const ws: Workspace = Object.assign({}, workspaceInEdition);
            ws.name = name;
            ws.db_connection = dbConnection;
            updateWorkspace(ws);
        }
        props.onClose();
    };

    return <>
        <MunityDialog title="Nom de projet" visible={props.show} onSave={saveWorkspace} onHide={props.onClose}>
            <div className="p-fluid">
                <div className="p-field p-grid">
                    <label htmlFor="name" className="p-col-12 p-md-2">Nom</label>
                    <div className="p-col-12 p-md-10">
                        <InputText className={errors.includes('name') ? 'p-invalid' : ''} id="name" type="text" value={name} onChange={(e) => setName(e.target.value)} />
                    </div>
                </div>
                <div className="p-field p-grid">
                    <label htmlFor="slug" className="p-col-12 p-md-2">Code</label>
                    <div className="p-col-12 p-md-10">
                        <InputText className={errors.includes('slug') ? 'p-invalid' : ''} readOnly={workspaceInEdition} id="slug" type="text" value={slug}
                            onChange={(e) => {
                                setSlugHasBeenSetByUser(true);
                                setSlug(slugify(e.target.value, {
                                    lower: true
                                }));
                            }}
                        />
                    </div>
                </div>
            </div>
        </MunityDialog>
    </>;
}

export default WorkspaceForm;
