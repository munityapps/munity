import React, { FunctionComponent, PropsWithChildren } from 'react';
import { Dialog } from 'primereact/dialog';
import { Button } from 'primereact/button';

const MunityDialog:FunctionComponent<PropsWithChildren<{visible:boolean, title:string, onSave:Function, onHide:Function}>> = props => {
    const footerButtons = <Button label="Save" icon="pi pi-check" onClick={() => {
        props.onSave();
        props.onHide();
    }} />;

    return <Dialog
        style={{ minWidth: '50vw' }}
        resizable={true}
        visible={props.visible}
        onHide={() => props.onHide()}
        maximizable={true}
        header={props.title}
        footer={footerButtons}
    >
        {props.children}
    </Dialog>;
}
export default MunityDialog;