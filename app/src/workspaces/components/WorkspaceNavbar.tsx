import { Button } from 'primereact/button';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faQuestionCircle, faBell } from '@fortawesome/free-regular-svg-icons'
import { Avatar } from 'primereact/avatar';
import { Menu } from 'primereact/menu';
import logo from '../../assets/logo.png';
import avatar from '../../assets/avatar_male.png';
import { useRef } from 'react';
import { useAppDispatch } from '../../hooks';
import { logout } from '../../authentication/slice';

import './WorkspaceNavbar.scss';
import { useHistory, useLocation } from 'react-router';

const WorkspaceNavbar = (props:{workspace:string|null}) => {
    let menu = useRef<Menu>(null);
    const dispatch = useAppDispatch();
    const location = useLocation();
    const history = useHistory();

    return <div className="navbar">
        <div className="left-part p-d-flex p-ai-center">
            <Button onClick={() => history.push('/')} className="p-button-link"><img src={logo} alt="logo" /></Button>
            <div className="workspace-name">{props.workspace}</div>
        </div>
        <div className="middle-part">
            <Button onClick={() => history.push(`/workspace/${props.workspace}/users`)} className={`p-button-link ${location.pathname.match(/^\/workspace\/[^/]+\/users/g) ? ' active' : ''}`}>Users</Button>
            <Button onClick={() => history.push(`/workspace/${props.workspace}/groups`)} className={`p-button-link ${location.pathname.match(/^\/workspace\/[^/]+\/groups/g) ? ' active' : ''}`}>Groups</Button>
        </div>
        <div className="right-part">
            <Button className="p-button-link">
                <FontAwesomeIcon icon={faQuestionCircle} />
            </Button>
            <Button className="p-button-link">
                <FontAwesomeIcon icon={faBell} />
            </Button>
            <div className="hi-message">
                Salut,&nbsp;<strong>Patrick</strong>
            </div>
            <Avatar shape="circle" image={avatar} />
            <Menu
                model={
                    [
                        {
                            label: 'Mon profile',
                            icon: 'pi pi-user-edit',
                            command: () => {
                                console.log({ severity: 'success', summary: 'Updated', detail: 'Data Updated', life: 3000 });
                            }
                        },
                        {
                            label: 'Déconnexion',
                            icon: 'pi pi-sign-out',
                            command: () => {
                                dispatch(logout())
                            }
                        },
                    ]
                }
                popup
                ref={menu}
            />
            <Button
                className="p-button-link "
                icon="pi pi-angle-down"
                onClick={(event) => menu.current?.toggle(event)}
                aria-controls="popup_menu"
                aria-haspopup
            />


        </div>
    </div>
};

export default WorkspaceNavbar;