import React from 'react';
import { FileUpload, FileUploadBeforeSendParams, FileUploadHandlerParam, FileUploadSelectParams, FileUploadUploadParams } from 'primereact/fileupload';
import { useAppSelector } from '../hooks';
import { getAPIUrl, getWorkspaceEndpoint } from '../helper';

const SimpleUploader: React.FC<{
    onUpload?:(e: FileUploadUploadParams) => void,
    onSelect?:(e: FileUploadSelectParams) => void,
    url?:string,
    maxFileSize?: number,
    uploadHandler?: Function,
    auto?: boolean,
}> = props => {
    const { JWTaccess } = useAppSelector(state => state.authentication)
    return <FileUpload
        mode="basic"
        name="file"
        url={props.url || `${getAPIUrl()}${getWorkspaceEndpoint('files/')}`}
        onBeforeSend={(e:FileUploadBeforeSendParams) => {
            e.xhr.setRequestHeader('authorization', `Bearer ${JWTaccess}`);
        }}
        uploadHandler={(e:FileUploadHandlerParam) => props?.uploadHandler && props.uploadHandler(e)}
        onSelect={(e:FileUploadSelectParams) => props?.onSelect && props.onSelect(e)}
        accept="image/*"
        maxFileSize={props.maxFileSize || 8000000}
        onUpload={props.onUpload}
        auto={props.auto}
        chooseLabel="Envoyer un fichier"
    />
}

export default SimpleUploader;
