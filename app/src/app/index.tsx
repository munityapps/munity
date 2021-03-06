// Libs
import React, { useEffect } from 'react';
import { Route, useLocation } from 'react-router';
import axios from 'axios';

// Tooling
import { useAppDispatch, useAppSelector } from '../hooks';
import { getAPIUrl } from '../helper';

// Redux
import { ready, setWorkspace } from './slice';

// Components
import AppRouter from './router';
import PermissionCheck from '../permissions/permissionCheck';
import NotificationManager from '../notifications';
import LoginForm from '../authentication';

const MunityApp: React.FC<{
    children: object,
    logoLogin: string,
    loadingWorkspace: React.FC,
    overmindSidebar: JSX.Element,
    overmindNavbar: JSX.Element,
    workspaceNavbar: JSX.Element,
    newOvermindRoutes: Partial<Route>[],
    newWorkspaceRoutes: Partial<Route>[],
    demoMode: boolean,
}> = props => {
    const dispatch = useAppDispatch();
    // isReady is redux ready and api url set
    const isReady = useAppSelector((state) => state.app.isReady);
    const { JWTaccess } = useAppSelector(state => state.authentication);
    const location = useLocation();

    // first initialisation step : set axios and defined workspace
    useEffect(() => {
        const pathname = location.pathname;
        const re = new RegExp('/workspace/([^/]+)');
        const result = pathname.match(re);
        const workspace = result ? result[1] : null;
        axios.defaults.baseURL = getAPIUrl();
        dispatch(setWorkspace(workspace));
        dispatch(ready());
    }, [dispatch, location.pathname]);

    if (!isReady) {
        return <props.loadingWorkspace/>;
    }

    return <>
        <NotificationManager key="notification-manager" />
        {!JWTaccess ? <LoginForm logo={props.logoLogin}/> :
            <PermissionCheck loadingWorkspace={props.loadingWorkspace}>
                <AppRouter
                    demoMode={props.demoMode}
                    loadingWorkspace={props.loadingWorkspace}
                    overmindSidebar = { props.overmindSidebar }
                    workspaceNavbar = { props.workspaceNavbar }
                    overmindNavbar = { props.overmindNavbar }
                    newOvermindRoutes = { props.newOvermindRoutes }
                    newWorkspaceRoutes = { props.newWorkspaceRoutes }
                >
                    {props.children}
                </AppRouter>
            </PermissionCheck>
        }
    </>
}

export default MunityApp;
