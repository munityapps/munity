import React, { useRef, useState } from 'react';
import { FileUpload, FileUploadBeforeSendParams, FileUploadHeaderTemplateOptions, FileUploadItemTemplateType, FileUploadProps, FileUploadSelectParams, FileUploadUploadParams } from 'primereact/fileupload';
import { ProgressBar } from 'primereact/progressbar';
import { Button } from 'primereact/button';
import { Tag } from 'primereact/tag';
import { addNotification } from '../notifications/slice';
import { useAppDispatch, useAppSelector } from '../hooks';
import { useTranslation } from 'react-i18next';

const PictureUploader: React.FC<FileUploadProps> = props => {
    const fileUploadRef = useRef<any>(null);
    const previewImg = useRef<HTMLImageElement>(null);
    const [totalSize, setTotalSize] = useState<number>(0);
    const dispatch = useAppDispatch();
    const { JWTaccess } = useAppSelector(state => state.authentication)
    const { t } = useTranslation();

    const onTemplateSelect = (e: FileUploadSelectParams) => {
        let _totalSize = totalSize;
        Array.from(e.files).forEach(file => {
            _totalSize = _totalSize + file.size;
        });

        setTotalSize(_totalSize);
    }

    const onTemplateUpload = (e: FileUploadUploadParams) => {
        let _totalSize = 0;
        Array.from(e.files).forEach(file => {
            _totalSize += (file.size || 0);
        });

        setTotalSize(_totalSize);
        dispatch(addNotification({ type: 'info', message: 'File Uploaded' }));
    }

    const onTemplateRemove = (file: File, callback: Function) => {
        setTotalSize(totalSize - file.size);
        callback();
    }

    const onTemplateClear = () => {
        setTotalSize(0);
    }

    const headerTemplate = (options: FileUploadHeaderTemplateOptions) => {
        const { className, chooseButton, uploadButton, cancelButton } = options;
        const value = totalSize / 10000;
        const formatedValue = fileUploadRef && fileUploadRef.current ? fileUploadRef.current.formatSize(totalSize) : '0 B';

        return (
            <div className={className} style={{ backgroundColor: 'transparent', display: 'flex', alignItems: 'center' }}>
                {chooseButton}
                {uploadButton}
                {cancelButton}
                <ProgressBar value={value} displayValueTemplate={() => `${formatedValue} / 1 MB`} style={{ width: '300px', height: '20px', marginLeft: 'auto' }}></ProgressBar>
            </div>
        );
    }


    const itemTemplate: FileUploadItemTemplateType = (file: File, props) => {
        const reader = new FileReader();
        reader.addEventListener("load", function () {
            // convert image file to base64 string
            if (previewImg?.current && (typeof reader.result === 'string') ) {
                previewImg.current.src = reader.result;
            }
        }, false);
        if (file) {
            reader.readAsDataURL(file);
        }
        return (
            <div className="p-d-flex p-ai-center p-flex-wrap">
                <div className="p-d-flex p-ai-center" style={{ width: '40%' }}>
                    <img ref={previewImg} src={undefined} alt={file.name} role="presentation" width={100} />
                    <span className="p-d-flex p-dir-col p-text-left p-ml-3">
                        {file.name}
                        <small>{new Date().toLocaleDateString()}</small>
                    </span>
                </div>
                <Tag value={props.formatSize} severity="warning" className="p-px-3 p-py-2" />
                <Button type="button" icon="pi pi-times" className="p-button-outlined p-button-rounded p-button-danger p-ml-auto" onClick={() => onTemplateRemove(file, props.onRemove)} />
            </div>
        )
    }

    const emptyTemplate = () => {
        return (
            <div className="p-d-flex p-ai-center p-dir-col">
                <i className="pi pi-image p-mt-3 p-p-5" style={{ 'fontSize': '5em', borderRadius: '50%', backgroundColor: 'var(--surface-b)', color: 'var(--surface-d)' }}></i>
                <span style={{ 'fontSize': '1.2em', color: 'var(--text-color-secondary)' }} className="p-my-5">{t('app:drag_and_drop')}</span>
            </div>
        )
    }

    const chooseOptions = { icon: 'pi pi-fw pi-images', iconOnly: true, className: 'custom-choose-btn p-button-rounded p-button-outlined' };
    const uploadOptions = { icon: 'pi pi-fw pi-cloud-upload', iconOnly: true, className: 'custom-upload-btn p-button-success p-button-rounded p-button-outlined' };
    const cancelOptions = { icon: 'pi pi-fw pi-times', iconOnly: true, className: 'custom-cancel-btn p-button-danger p-button-rounded p-button-outlined' };


    return <FileUpload
        ref={fileUploadRef}
        name="fileUpload[]"
        url={props.url}
        onBeforeSend={(e:FileUploadBeforeSendParams) => {
            e.xhr.setRequestHeader('Authentication', `Bearer ${JWTaccess}`);
        }}
        multiple
        accept="image/*"
        maxFileSize={props.maxFileSize || 1000000}
        onUpload={onTemplateUpload}
        onSelect={onTemplateSelect}
        onError={onTemplateClear}
        onClear={onTemplateClear}
        headerTemplate={headerTemplate}
        itemTemplate={itemTemplate}
        emptyTemplate={emptyTemplate}
        chooseOptions={chooseOptions}
        uploadOptions={uploadOptions}
        cancelOptions={cancelOptions}
    />
}

export default PictureUploader;
