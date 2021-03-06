import { Button } from 'primereact/button';
import { Avatar } from 'primereact/avatar';
import { Menu } from 'primereact/menu';
import { useRef, useState } from 'react';
import { useAppDispatch, useAppSelector } from '../../../hooks';
import { logout } from '../../../authentication/slice';
import UserForm from '../../../user/form';
import { getURLForFile } from '../../../helper';
import { setUserInEdition } from '../../../user/slice';
import { useTranslation } from 'react-i18next';

const NavbarRight = () => {
    let menu = useRef<Menu>(null);
    const dispatch = useAppDispatch();
    const currentUser = useAppSelector(state => state.authentication.currentUser)
    const [showForm, setShowForm] = useState<boolean>(false);
    const { t } = useTranslation();

    return <div className="right-part">
        <div className="hi-message">
            {t('common:hi')}, &nbsp;<strong>{currentUser?.username}</strong>
        </div>
        <UserForm show={showForm} onClose={() => {setShowForm(false);dispatch(setUserInEdition(null))}}/>
        { currentUser.avatar ?
            <Avatar shape="circle" className="p-mr-2" image={getURLForFile(currentUser.avatar.file)} /> :
            <Avatar shape="circle" icon="pi pi-user" className="p-mr-2" />
        }
        <Menu
            model={
                [
                    {
                        label: t('common:profil'),
                        icon: 'pi pi-user-edit',
                        command: () => {
                            setShowForm(true);
                            dispatch(setUserInEdition(currentUser));
                        }
                    },
                    {
                        label: t('common:logout'),
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
