import 'react-toastify/dist/ReactToastify.css';

import munityLogo from '../../assets/logoIcon.png';
import iconOvmGraph from '../../assets/icon_ovm_graph.svg';
import iconOvmAdmin from '../../assets/icon_ovm_admin.svg';
import iconOvmInt from '../../assets/icon_ovm_int.svg';
import iconOvmDeploy from '../../assets/icon_ovm_deploy.svg';
import { Button } from 'primereact/button';
import { useAppDispatch } from '../../hooks';
import { addNotification } from '../../notifications/slice';
import { useHistory, useLocation } from 'react-router';
import React from 'react';
import { useTranslation } from 'react-i18next';

const OvermindSidebar: React.FC<{newMenuButton?:Partial<React.Component>[]}> = props => {

    const dispatch = useAppDispatch();
    const location = useLocation();
    const history = useHistory();

    const { t } = useTranslation();

    const featureInative = () => {
        dispatch(addNotification({
            type: 'info',
            message: <div style={{ display: 'flex', alignItems: 'center' }}>
                <img style={{ height: '60px' }} src={munityLogo} alt="munityLogo" />
                <div>{t('app:you_need')}<a href="https://munityapps.com">
                    Munity Portal</a> {t('app:to_access_feature')}.
                </div>
            </div>
        }));
    };
    return <div className="sidebar">
        <div className="project">
            <img src={munityLogo} alt="logo" />
            <div>
                <div className="legend">{t('common:project_name')}</div>
                <div className="project-name">Munity</div>
            </div>
        </div>
        <div className="menu">
            <Button className={`p-button-link ${location.pathname.match(/^\/?$/g) ? 'active' : null}`} onClick={() => history.push('/')}>
                <img src={iconOvmGraph} alt="graph" /> {t('common:monitoring')}
            </Button>
        </div>
        <div className="menu">
            <Button className={`p-button-link ${location.pathname.match(/^\/workspaces/g) ? 'active' : null}`} onClick={() => history.push('/workspaces')}>
                <img style={{ marginRight: '30px' }} src={iconOvmDeploy} alt="graph" /> {t('common:customers')}
            </Button>
        </div>
        <div className="menu">
            <Button className={`p-button-link ${location.pathname.match(/^\/users/g) ? 'active' : null}`} onClick={() => history.push('/users')}>
                <img src={iconOvmAdmin} alt="graph" /> {t('common:administrator')}
            </Button>
        </div>
        <div className="menu">
            <Button className="p-button-link disabled" onClick={featureInative}>
                <img src={iconOvmInt} alt="graph" /> {t('common:integration')}
            </Button>
        </div>
        <div className="menu">
            <Button className="p-button-link disabled" onClick={featureInative}>
                <img src={iconOvmGraph} alt="graph" /> {t('common:deployment')}
            </Button>
        </div>
        {props.newMenuButton}
    </div>
}

export default OvermindSidebar;
