var __assign = (this && this.__assign) || function () {
    __assign = Object.assign || function(t) {
        for (var s, i = 1, n = arguments.length; i < n; i++) {
            s = arguments[i];
            for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p))
                t[p] = s[p];
        }
        return t;
    };
    return __assign.apply(this, arguments);
};
import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Button } from 'primereact/button';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faQuestionCircle, faBell } from '@fortawesome/free-regular-svg-icons';
import { Avatar } from 'primereact/avatar';
import { Menu } from 'primereact/menu';
import logo from '../../assets/logo.png';
import avatar from '../../assets/avatar_male.png';
import { useRef } from 'react';
import { useAppDispatch } from '../../hooks';
import { logout } from '../../authentication/slice';
import './OvermindNavbar.scss';
import { useHistory, useLocation } from 'react-router';
var Navbar = function () {
    var menu = useRef(null);
    var dispatch = useAppDispatch();
    var location = useLocation();
    var history = useHistory();
    return _jsxs("div", __assign({ className: "navbar" }, { children: [_jsx("div", __assign({ className: "left-part p-d-flex p-ai-center" }, { children: _jsx(Button, __assign({ onClick: function () { return history.push('/'); }, className: "p-button-link" }, { children: _jsx("img", { src: logo, alt: "logo" }, void 0) }), void 0) }), void 0), _jsxs("div", __assign({ className: "middle-part" }, { children: [_jsx(Button, __assign({ onClick: function () { return history.push('/workspaces'); }, className: "p-button-link " + (location.pathname.match(/^\/workspaces/g) ? ' active' : '') }, { children: "Workspaces" }), void 0), _jsx(Button, __assign({ onClick: function () { return history.push('/users'); }, className: "p-button-link " + (location.pathname.match(/^\/users/g) ? ' active' : '') }, { children: "Users" }), void 0)] }), void 0), _jsxs("div", __assign({ className: "right-part" }, { children: [_jsx(Button, __assign({ className: "p-button-link" }, { children: _jsx(FontAwesomeIcon, { icon: faQuestionCircle }, void 0) }), void 0), _jsx(Button, __assign({ className: "p-button-link" }, { children: _jsx(FontAwesomeIcon, { icon: faBell }, void 0) }), void 0), _jsxs("div", __assign({ className: "hi-message" }, { children: ["Salut,\u00A0", _jsx("strong", { children: "Patrick" }, void 0)] }), void 0), _jsx(Avatar, { shape: "circle", image: avatar }, void 0), _jsx(Menu, { model: [
                            {
                                label: 'Mon profile',
                                icon: 'pi pi-user-edit',
                                command: function () {
                                    console.log({ severity: 'success', summary: 'Updated', detail: 'Data Updated', life: 3000 });
                                }
                            },
                            {
                                label: 'Déconnexion',
                                icon: 'pi pi-sign-out',
                                command: function () {
                                    dispatch(logout());
                                }
                            },
                        ], popup: true, ref: menu }, void 0), _jsx(Button, { className: "p-button-link ", icon: "pi pi-angle-down", onClick: function (event) { var _a; return (_a = menu.current) === null || _a === void 0 ? void 0 : _a.toggle(event); }, "aria-controls": "popup_menu", "aria-haspopup": true }, void 0)] }), void 0)] }), void 0);
};
export default Navbar;
