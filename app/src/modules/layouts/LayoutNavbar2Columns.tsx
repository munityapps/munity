import { useTranslation } from 'react-i18next';
import { LayoutConfiguration } from '../core/components/LayoutDispatcher';

import './LayoutNavbar2Columns.scss';

const LayoutNavbar2Columns = (props: LayoutConfiguration) => {
    const { t } = useTranslation();
    console.log(props);

    return <div className="layout-navbar-2-columns p-d-flex p-flex-column">
        { props.navbarSlot }
        <div className={'p-d-flex p-flex-row main-content'}>
            <div className="left-column p-d-flex p-ai-center p-jc-center">
                { props.leftPanelSlot }
            </div>
            <div className="right-column p-d-flex p-ai-center p-jc-center">
                { props.rightPanelSlot }
            </div>
        </div>
    </div>
}

export default LayoutNavbar2Columns;
