import { useEffect } from 'react';

import LoadingApp from '../layouts/components/LoadingApp';
import LoginForm from '../authentication';
import NotificationManager from '../notifications';

import { useAppDispatch, useAppSelector } from '../hooks';

import { ready } from './slice';

import { Route, Switch } from 'react-router';
import Workspace from '../workspaces';
import Overmind from '../overmind';
import axios from 'axios';
import { getDefaultAPIUrl } from '../helper';

const MunityApp = (props: {
    children: object,
    navbar: Partial<React.Component>,
    newOvermindRoutes: Partial<Route>[],
    newWorkspaceRoutes: Partial<Route>[]
}) => {
    const dispatch = useAppDispatch();
    const isReady = useAppSelector((state) => state.app.isReady);
    const access = useAppSelector((state) => state.auhentication.access);

    useEffect(() => {
        axios.defaults.baseURL = getDefaultAPIUrl();
    }, [])

    useEffect(() => {
        setTimeout(() => {
            dispatch(ready());
        }, 1000);
    }, [dispatch]);

    const AppRouter = <>
        {props.navbar}
        <Switch>
            {props.children}
            <Route path="/workspace/:workspace_slug" children={<Workspace newRoutes={props.newWorkspaceRoutes}/>} />
            <Route path="/" children={<Overmind newRoutes={props.newOvermindRoutes}/>}/>
        </Switch>
    </>;

    return <>
        <NotificationManager key="notification-manager" />
        {!isReady ? <LoadingApp /> : (access ? AppRouter : <LoginForm />)}
    </>
}

export default MunityApp;
