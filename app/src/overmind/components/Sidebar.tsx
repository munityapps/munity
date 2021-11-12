import 'react-toastify/dist/ReactToastify.css';
import { FunctionComponent } from 'react';

import munityLogo from '../../assets/logoIcon.png';
import iconOvmGraph from '../../assets/icon_ovm_graph.svg';
import iconOvmAdmin from '../../assets/icon_ovm_admin.svg';
import iconOvmInt from '../../assets/icon_ovm_int.svg';
import iconOvmDeploy from '../../assets/icon_ovm_deploy.svg';
import { Button } from 'primereact/button';
import { useAppDispatch } from '../../hooks';
import { addNotification } from '../../notifications/slice';
import { useHistory, useLocation } from 'react-router';

const OvermindSidebar: FunctionComponent<{}> = () => {

    const dispatch = useAppDispatch();
    const location = useLocation();
    const history = useHistory();

    const featureInative = () => {
        dispatch(addNotification({
            type: 'info',
            message: <div style={{ display: 'flex', alignItems: 'center' }}>
                <img style={{ height: '60px' }} src={munityLogo} alt="munityLogo" />
                <div>You need <a href="https://munityapps.com">
                    Munity Portal</a> to access this feature.
                </div>
            </div>
        }));
    };
    return <div className="sidebar">
        <div className="project">
            <img src={munityLogo} alt="logo" />
            <div>
                <div className="legend">Your project name</div>
                <div className="project-name">Demo</div>
            </div>
        </div>
        <div className="menu">
            <Button className={`p-button-link ${location.pathname.match(/^\/?$/g) ? 'active' : null}`} onClick={() => history.push('/')}>
                <img src={iconOvmGraph} alt="graph" /> Monitoring
            </Button>
        </div>
        <div className="menu">
            <Button className={`p-button-link ${location.pathname.match(/^\/workspaces/g) ? 'active' : null}`} onClick={() => history.push('/workspaces')}>
                <img style={{ marginRight: '30px' }} src={iconOvmDeploy} alt="graph" /> Customers
            </Button>
        </div>
        <div className="menu">
            <Button className={`p-button-link ${location.pathname.match(/^\/users/g) ? 'active' : null}`} onClick={() => history.push('/users')}>
                <img src={iconOvmAdmin} alt="graph" /> Administrators
            </Button>
        </div>
        <div className="menu">
            <Button className="p-button-link disabled" onClick={featureInative}>
                <img src={iconOvmInt} alt="graph" /> Integration
            </Button>
        </div>
        <div className="menu">
            <Button className="p-button-link disabled" onClick={featureInative}>
                <img src={iconOvmGraph} alt="graph" /> Deployment
            </Button>
        </div>
    </div>
}

export default OvermindSidebar;
