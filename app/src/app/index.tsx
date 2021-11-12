import React, { useEffect } from 'react';

import LoadingMunity from '../layouts/components/LoadingMunity';
import LoginForm from '../authentication';
import NotificationManager from '../notifications';

import { useAppDispatch, useAppSelector } from '../hooks';

import jwtDecode from 'jwt-decode';
import { ready } from './slice';

import { Route, Switch } from 'react-router';
import Workspace from '../workspaces';
import Overmind from '../overmind';
import axios from 'axios';
import { getDefaultAPIUrl } from '../helper';
import { useGetUsersQuery, User } from '../user/slice';
import { setCurrentUser } from '../authentication/slice';

const MunityApp = (props: {
    children: object,
    loadingWorkspace: React.FC,
    workspaceNavbar: Partial<React.Component>,
    newOvermindRoutes: Partial<Route>[],
    newWorkspaceRoutes: Partial<Route>[]
}) => {
    const dispatch = useAppDispatch();
    const isReady = useAppSelector((state) => state.app.isReady);
    const access = useAppSelector((state) => state.authentication.access);

    useEffect(() => {
        axios.defaults.baseURL = getDefaultAPIUrl();
    }, [])

    useEffect(() => {
        setTimeout(() => {
            dispatch(ready());
        }, 1000);
    }, [dispatch]);

    const AppRouter: React.FC = () => {
        // get user when app ready
        const { data: users } = useGetUsersQuery();
        useEffect(() => {
            const jwtData: { exp: string, jti: string, token_type: string, user_id: string } = jwtDecode(access);
            const user: User | null = users?.results.find(u => {
                return u.id === jwtData.user_id
            }) || null;
            dispatch(setCurrentUser(user));
        }, [users]);
        return <>
            <Switch>
                {props.children}
                <Route path="/workspace/:workspace_slug" children={<Workspace navbar={props.workspaceNavbar} newRoutes={props.newWorkspaceRoutes} />} />
                <Route path="/" children={<Overmind newRoutes={props.newOvermindRoutes} />} />
            </Switch>
        </>;
    }

    const LoadingApp = () => {
        return <Switch>
            <Route path="/workspace/:workspace_slug" component={LoadingMunity} />
            <Route path="/" component={props.loadingWorkspace} />
        </Switch>;
    }

    return <>
        <NotificationManager key="notification-manager" />
        {!isReady ? <LoadingApp /> : (access ? <AppRouter /> : <LoginForm />)}
    </>
}

export default MunityApp;
