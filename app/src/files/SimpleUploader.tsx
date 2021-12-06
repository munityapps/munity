import React from 'react';
import { FileUpload, FileUploadBeforeSendParams, FileUploadHandlerParam, FileUploadSelectParams, FileUploadUploadParams } from 'primereact/fileupload';
import { useAppSelector } from '../hooks';
import { getAPIUrl, getWorkspaceEndpoint } from '../helper';
import { useTranslation } from 'react-i18next';

const SimpleUploader: React.FC<{
    onUpload?:(e: FileUploadUploadParams) => void,
    onSelect?:(e: FileUploadSelectParams) => void,
    label?:string,
    url?:string,
    accept?:string,
    maxFileSize?: number,
    uploadHandler?: Function,
    auto?: boolean,
}> = props => {
    const { JWTaccess } = useAppSelector(state => state.authentication)
    const { t } = useTranslation();
    return <FileUpload
        mode="basic"
        name="file"
        url={props.url || `${getAPIUrl()}${getWorkspaceEndpoint('/files/')}`}
        onBeforeSend={(e:FileUploadBeforeSendParams) => {
            e.xhr.setRequestHeader('authorization', `Bearer ${JWTaccess}`);
        }}
        uploadHandler={(e:FileUploadHandlerParam) => props?.uploadHandler && props.uploadHandler(e)}
        onSelect={(e:FileUploadSelectParams) => props?.onSelect && props.onSelect(e)}
        accept={props.accept || "*/*"}
        maxFileSize={props.maxFileSize || 8000000}
        onUpload={props.onUpload}
        auto={props.auto}
        chooseLabel={props.label ? props.label : t('app:send_a_file')}
    />
}

export default SimpleUploader;
