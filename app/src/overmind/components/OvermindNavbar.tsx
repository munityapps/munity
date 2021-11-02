import { Button } from 'primereact/button';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faQuestionCircle, faBell } from '@fortawesome/free-regular-svg-icons'
import { Avatar } from 'primereact/avatar';
import { Menu } from 'primereact/menu';
import logo from '../../assets/logo.png';
import { useRef } from 'react';
import { useAppDispatch } from '../../hooks';
import { logout } from '../../authentication/slice';

import './OvermindNavbar.scss';
import { useHistory, useLocation } from 'react-router';

const Navbar = () => {
    let menu = useRef<Menu>(null);
    const dispatch = useAppDispatch();
    const location = useLocation();
    const history = useHistory();

    return <div className="navbar">
        <div className="left-part p-d-flex p-ai-center">
            <Button onClick={() => history.push('/')} className="p-button-link"><img src={logo} alt="logo" /></Button>
        </div>
        <div className="middle-part">
            <Button  onClick={() => history.push('/workspaces')} className={`p-button-link ${location.pathname.match(/^\/workspaces/g) ? ' active' : ''}`}>Workspaces</Button>
            <Button  onClick={() => history.push('/users')} className={`p-button-link ${location.pathname.match(/^\/users/g) ? ' active' : ''}`}>Users</Button>
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
            <Avatar shape="circle" icon="pi pi-user" />
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

export default Navbar;