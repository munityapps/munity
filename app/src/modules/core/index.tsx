import { useEffect } from 'react';

import LoadingApp from './components/LoadingApp';
import LoginForm from '../authentication';
import NotificationManager from '../notifications';

import { useAppDispatch, useAppSelector } from '../../hooks';

import { ready } from './slice';

import './style.scss';
import { Route, Switch } from 'react-router';
import Workspace from '../workspaces';
import Overmind from '../overmind';
import axios from 'axios';
import { getDefaultAPIUrl } from '../../helper';

const Core = () => {
    const dispatch = useAppDispatch();
    const isReady = useAppSelector((state) => state.core.isReady);
    const access = useAppSelector((state) => state.auhentication.access);

    const { primaryColor, primaryColorText, secondaryColor,
        textColor, textColorSecondary,
        contentPadding, inlineSpacing,
        surfaceA, surfaceB, surfaceC, surfaceD,
        errorColor, validColor,
    } = useAppSelector(state => state.core);

    // -------
    // TO REMOVE
    useEffect(() => {
        if (primaryColor) document.documentElement.style.setProperty("--primary-color", primaryColor);
        if (primaryColorText) document.documentElement.style.setProperty("--primary-color-text", primaryColorText);
        if (secondaryColor) document.documentElement.style.setProperty("--secondary-color", secondaryColor);
        if (textColor) document.documentElement.style.setProperty("--text-color", textColor);
        if (textColorSecondary) document.documentElement.style.setProperty("--text-color-secondary", textColorSecondary);
        if (contentPadding) document.documentElement.style.setProperty("--content-padding", contentPadding);
        if (inlineSpacing) document.documentElement.style.setProperty("--inline-spacing", inlineSpacing);
        if (surfaceA) document.documentElement.style.setProperty("--surface-a", surfaceA);
        if (surfaceB) document.documentElement.style.setProperty("--surface-b", surfaceB);
        if (surfaceC) document.documentElement.style.setProperty("--surface-c", surfaceC);
        if (surfaceD) document.documentElement.style.setProperty("--surface-d", surfaceD);
        if (errorColor) document.documentElement.style.setProperty("--error-color", errorColor);
        if (validColor) document.documentElement.style.setProperty("--valid-color", validColor);
    }, [
        primaryColor, primaryColorText, secondaryColor,
        textColor, textColorSecondary,
        contentPadding, inlineSpacing,
        surfaceA, surfaceB, surfaceC, surfaceD,
        errorColor, validColor,
    ]);
    // TO REMOVE
    // -------

    useEffect(() => {
        axios.defaults.baseURL = getDefaultAPIUrl();
    }, [])

    useEffect(() => {
        setTimeout(() => {
            dispatch(ready());
        }, 1000);
    }, [dispatch]);

    const router = <Switch>
        <Route path="/workspace/:workspace_slug" component={Workspace} />
        <Route path="/" component={Overmind} />
    </Switch>;

    return <>
        <NotificationManager key="notification-manager" />
        {!isReady ? <LoadingApp /> : (access ? router : <LoginForm />)}
    </>
}

export default Core;
