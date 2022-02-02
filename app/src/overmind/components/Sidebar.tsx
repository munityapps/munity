import 'react-toastify/dist/ReactToastify.css';

import munityLogo from '../../assets/logo512.png';
import keyossLogo from '../../assets/keyos.png';
import iconOvmGraph from '../../assets/icon_ovm_graph.svg';
import iconOvmAdmin from '../../assets/icon_ovm_admin.svg';
import iconOvmDeploy from '../../assets/icon_ovm_deploy.svg';
import { Button } from 'primereact/button';
import { InputText } from 'primereact/inputtext';
import { Dialog } from 'primereact/dialog';
import { useAppDispatch } from '../../hooks';
import { addNotification } from '../../notifications/slice';
import { useHistory, useLocation } from 'react-router';
import React from 'react';
import { useTranslation } from 'react-i18next';
import { faDiscord, faGitAlt } from '@fortawesome/free-brands-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';

const OvermindSidebar: React.FC<{ newMenuButton?: Partial<React.Component>[] }> = props => {

    const dispatch = useAppDispatch();
    const location = useLocation();
    const history = useHistory();

    const [showGitPopup, setShowGitPopup] = React.useState<boolean>(false);

    const { t } = useTranslation();

    return <div className="sidebar">
        <div className="project">
            <img src={keyossLogo} alt="logo" />
            <div>
                <div className="legend">{t('common:project_name')}</div>
                <div className="project-name">Keyoss</div>
            </div>
        </div>
        <div className="menu">
            <Button className={`p-button-link ${location.pathname.match(/^\/$/g) ? 'active' : null}`} onClick={() => history.push('/')}>
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
        <div className="download">
            <Button className="p-shadow-4" onClick={() => setShowGitPopup(true)}>
                <FontAwesomeIcon icon={faGitAlt} /> {t('common:get_source_code')}
            </Button>
        </div>
        <Dialog header="Clone your project" visible={showGitPopup} style={{ width: '50vw' }} footer={() => { }} onHide={() => setShowGitPopup(false)}>
            <div style={{ fontStyle: 'italic' }}>You can clone your project from here :</div>
            <div className="download-link p-inputgroup">
                <span className="p-inputgroup-addon"> <FontAwesomeIcon icon={faGitAlt} size="lg" color="#E84E31" /></span>
                <InputText style={{ backgroundColor: 'lightgray', margin: '10px 0px', border: '1px solid black' }} value="git@github.com:munityapps/keysaas.git" />
            </div>
            <div className="terminal-demo">
                <div className="card">
                    <div className="p-terminal">
                        <p>
                            <span className="p-terminal-prompt">user@home:~/myproject $</span> <span className="p-terminal-command">mkdir keysaas ; git clone https://github.com/munityapps/keysaas keysaas</span>
                        </p>
                        <p>
                            <span className="p-terminal-response">Cloning into 'keysaas'...</span>
                        </p>
                        <p>
                            <span className="p-terminal-prompt">user@home:~/myproject $</span> <span className="p-terminal-command">cd keysaas && cp .env.sample .env && vi .env</span>
                        </p>
                        <p>
                            <span className="p-terminal-prompt">user@home:~/myproject $</span> <span className="p-terminal-command">./script/start.sh</span>
                        </p>
                        <p>
                            <span className="p-terminal-response">
                                Starting munity_db_1      ... <span style={{ color: 'green' }}>done</span><br />
                                Starting munity_traefik_1 ... <span style={{ color: 'green' }}>done</span><br />
                                Starting munity_api_1     ... <span style={{ color: 'green' }}>done</span><br />
                                Starting munity_app_1     ... <span style={{ color: 'green' }}>done</span><br /><br />
                                Username : <br />
                                [...]
                            </span>
                        </p>
                    </div>
                </div>
            </div>

            <p>
                You can clone your project from Munity server to develop on top of it in your prefered development environment.<br />
                Send us back your code <strong style={{ color: '#5F00EF' }}>by pushing master branch</strong> when you are satisfied and we will update your application with your fresh new improvments and features.
            </p>
            <p>
                <div className="p-d-flex p-ai-center" style={{ marginTop: '16px' }}>
                    <img alt="munityLogo" width="50px" src={munityLogo} />
                    <div style={{ padding: '10px' }}>
                        You will find help to create your buisness layer by following Munity documentation here : <a style={{ color: '#5F00EF', fontWeight: 'bold' }} href="https://doc.munityapps.com/" target="_blank">READ THE DOC!</a> <br />
                    </div>
                </div>
                <div className="p-d-flex p-ai-center" style={{ marginTop: '32px' }}>
                    <FontAwesomeIcon icon={faDiscord} style={{ fontSize: '45px' }} color="#5865F2" />
                    <div style={{ padding: '10px' }}>
                        And you can also join our wonderfull community on Discord here : <a style={{ color: '#5F00EF', fontWeight: 'bold' }} href="https://discord.gg/n2Q6FraW" target="_blank">JOIN US!</a>
                    </div>
                </div>
            </p>
        </Dialog>
        {props.newMenuButton}
    </div>
}

export default OvermindSidebar;
