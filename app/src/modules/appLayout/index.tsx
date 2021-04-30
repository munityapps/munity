import { InputText } from 'primereact/inputtext';
import { Button } from 'primereact/button';
import { InputTextarea } from 'primereact/inputtextarea';

import { useAppSelector, useAppDispatch } from '../../hooks';

// Actions
import {ready as appIsReady} from '../core/coreSlice';

import './styles.scss';

const AppLayout = (props: {[key: string]: {[key:string]: string}}) => {
    const dispatch = useAppDispatch();
    const isReady = useAppSelector(state => state.core.ready);

    return <div id="app-layout" className={'p-d-flex p-flex-row'}>
        <div id="app-layout-left-section" className={'p-d-flex'}>
            SIDEBAR
        </div>
        <div id="app-layout-center-section" className={'p-d-flex p-flex-column'}>
            <div id="app-layout-center-top-section" className={'p-d-flex'}>
                NAVBAR
            </div>
            <div id="app-layout-center-middle-section" className={'p-d-flex'}>
                <div className="p-fluid p-formgrid p-grid">
                    <div className="p-field p-col-12 p-md-6">
                        <label htmlFor="firstname6">Firstname</label>
                        <InputText id="firstname6" type="text" />
                    </div>
                    <div className="p-field p-col-12 p-md-6">
                        <label htmlFor="address">Address</label>
                        <InputTextarea id="address" rows={4} />
                    </div>
                    <div className="p-field p-col-12">
                        { isReady ? <strong>ON</strong> : <strong>OFF</strong>}
                        <Button onClick={() => dispatch(appIsReady())}>
                            Dispatch!
                        </Button>
                    </div>
                </div>
            </div>
            <div id="app-layout-center-bottom-section" className={'p-d-flex'}>
                FOOTBAR
            </div>
        </div>
        <div id="app-layout-right-section" className={'p-d-flex '}>
        </div>
    </div>;
}

export default AppLayout;
