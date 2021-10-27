import { jsx as _jsx, jsxs as _jsxs, Fragment as _Fragment } from "react/jsx-runtime";
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
var MunityRouter = function (props) {
    var dispatch = useAppDispatch();
    var isReady = useAppSelector(function (state) { return state.app.isReady; });
    var access = useAppSelector(function (state) { return state.auhentication.access; });
    useEffect(function () {
        axios.defaults.baseURL = getDefaultAPIUrl();
    }, []);
    useEffect(function () {
        setTimeout(function () {
            dispatch(ready());
        }, 1000);
    }, [dispatch]);
    var AppRouter = _jsxs(Switch, { children: [props.children, _jsx(Route, { path: "/workspace/:workspace_slug", component: Workspace }, void 0), _jsx(Route, { path: "/", component: Overmind }, void 0)] }, void 0);
    return _jsxs(_Fragment, { children: [_jsx(NotificationManager, {}, "notification-manager"), !isReady ? _jsx(LoadingApp, {}, void 0) : (access ? AppRouter : _jsx(LoginForm, {}, void 0))] }, void 0);
};
export default MunityRouter;
