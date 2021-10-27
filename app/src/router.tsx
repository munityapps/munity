import { useEffect } from 'react';

import LoadingApp from './layouts/components/LoadingApp';
import LoginForm from './authentication';
import NotificationManager from './notifications';

import { useAppDispatch, useAppSelector } from './hooks';

import { ready } from './app/slice';

import { Route, Switch } from 'react-router';
import Workspace from './workspaces';
import Overmind from './overmind';
import axios from 'axios';
import { getDefaultAPIUrl } from './helper';

const MunityRouter = (props: { children: object }) => {
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

    const AppRouter = <Switch>
        {props.children}
        <Route path="/workspace/:workspace_slug" component={Workspace} />
        <Route path="/" component={Overmind} />
    </Switch>;

    return <>
        <NotificationManager key="notification-manager" />
        {!isReady ? <LoadingApp /> : (access ? AppRouter : <LoginForm />)}
    </>
}

export default MunityRouter;
