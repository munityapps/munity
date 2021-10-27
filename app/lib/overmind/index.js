import { jsx as _jsx, jsxs as _jsxs, Fragment as _Fragment } from "react/jsx-runtime";
import { Route, Switch } from 'react-router';
import 'react-toastify/dist/ReactToastify.css';
import LayoutDispatcher from '../layouts/LayoutDispatcher';
import User from '../user';
import Navbar from './components/OvermindNavbar';
import OvermindWorkspaces from './components/OvermindWorkspaces';
var Overmind = function () {
    return _jsx(LayoutDispatcher, { layoutName: "TwoColumns", navbarSlot: _jsx(Navbar, {}, void 0), mainSlot: _jsx(_Fragment, { children: _jsxs(Switch, { children: [_jsx(Route, { path: "/workspaces", component: OvermindWorkspaces }, void 0), _jsx(Route, { path: "/users", component: User }, void 0), _jsx(Route, { path: "/", component: function () { return _jsx("div", { children: "This is overmind !" }, void 0); } }, void 0)] }, void 0) }, void 0) }, void 0);
};
export default Overmind;
