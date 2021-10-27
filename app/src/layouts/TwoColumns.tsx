// import { useTranslation } from 'react-i18next';
import { LayoutConfiguration } from '../layouts/LayoutDispatcher';

import './TwoColumns.scss';

const TwoColumns = (props: LayoutConfiguration) => {
    // const { t } = useTranslation();

    return <div className="layout-navbar-2-columns p-d-flex p-flex-column">
        { props.navbarSlot }
        <div className={'p-d-flex p-flex-row main-content'}>
            <div className="left-column p-d-flex p-ai-center p-jc-center">
                { props.mainSlot }
            </div>
            <div className="right-column p-d-flex p-ai-center p-jc-center">
                { props.rightPanelSlot }
            </div>
        </div>
    </div>
}

export default TwoColumns;
