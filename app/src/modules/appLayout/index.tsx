import { InputText } from 'primereact/inputtext';
import { Dropdown } from 'primereact/dropdown';
import { InputTextarea } from 'primereact/inputtextarea';

import './styles.scss';


const citySelectItems = [
    {label: 'New York', value: 'NY'},
    {label: 'Rome', value: 'RM'},
    {label: 'London', value: 'LDN'},
    {label: 'Istanbul', value: 'IST'},
    {label: 'Paris', value: 'PRS'}
];

const AppLayout = (props: {[key: string]: {[key:string]: string}}) => {
    return <div id="app-layout" className={'p-d-flex p-flex-row'}>
        <div id="app-layout-left-section" className={'p-d-flex'}>
            LEFT SECTION
        </div>
        <div id="app-layout-center-section" className={'p-d-flex p-flex-column'}>
            <div id="app-layout-center-top-section" className={'p-d-flex'}>
                CENTER TOP SECTION
            </div>
            <div id="app-layout-center-middle-section" className={'p-d-flex'}>
                CENTER MIDDLE SECTION
                <div className="p-fluid p-formgrid p-grid">
                    <div className="p-field p-col-12 p-md-6">
                        <label htmlFor="firstname6">Firstname</label>
                        <InputText id="firstname6" type="text" />
                    </div>
                    <div className="p-field p-col-12 p-md-6">
                        <label htmlFor="lastname6">Lastname</label>
                        <InputText id="lastname6" type="text" />
                    </div>
                    <div className="p-field p-col-12">
                        <label htmlFor="address">Address</label>
                        <InputTextarea id="address" rows={4} />
                    </div>
                    <div className="p-field p-col-12 p-md-6">
                        <label htmlFor="city">City</label>
                        <InputText id="city" type="text" />
                    </div>
                    <div className="p-field p-col-12 p-md-3">
                        <label htmlFor="state">State</label>
                        <Dropdown inputId="state" options={citySelectItems} placeholder="Select" optionLabel="name"/>
                    </div>
                    <div className="p-field p-col-12 p-md-3">
                        <label htmlFor="zip">Zip</label>
                        <InputText id="zip" type="text" />
                    </div>
                </div>
            </div>
            <div id="app-layout-center-bottom-section" className={'p-d-flex'}>
                CENTER BOTTOM SECTION
            </div>
        </div>
        <div id="app-layout-right-section" className={'p-d-flex '}>
            RIGHT SECTION
        </div>
    </div>;
}

export default AppLayout;
