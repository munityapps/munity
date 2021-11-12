import { Button } from 'primereact/button';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faQuestionCircle, faBell } from '@fortawesome/free-regular-svg-icons'
import { Avatar } from 'primereact/avatar';
import { Menu } from 'primereact/menu';
import { useRef } from 'react';
import { useAppDispatch, useAppSelector } from '../../../hooks';
import { logout } from '../../../authentication/slice';

const NavbarRight = () => {
    let menu = useRef<Menu>(null);
    const dispatch = useAppDispatch();
    const currentUser = useAppSelector(state => state.authentication.currentUser)

    return <div className="right-part">
        {/* <Button className="p-button-link">
            <FontAwesomeIcon icon={faQuestionCircle} />
        </Button>
        <Button className="p-button-link">
            <FontAwesomeIcon icon={faBell} />
        </Button> */}
        <div className="hi-message">
            Hi,&nbsp;<strong>{currentUser?.username}</strong>
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
};

export default NavbarRight;
