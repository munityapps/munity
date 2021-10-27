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
import { Button } from "primereact/button";
import { Divider } from "primereact/divider";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faTrash, faUserEdit, faUserPlus } from "@fortawesome/free-solid-svg-icons";
import { useDeleteUserMutation, useGetUsersQuery } from "./slice";
var UserList = function (props) {
    var users = useGetUsersQuery().data;
    var deleteUser = useDeleteUserMutation()[0];
    return _jsxs("div", { children: [users === null || users === void 0 ? void 0 : users.results.map(function (user) {
                return _jsxs("div", { children: [_jsx("div", { children: user.username }, user.id), _jsx(Button, __assign({ className: "p-button", onClick: function () { return props.setEditUser(user); } }, { children: _jsx(FontAwesomeIcon, { icon: faUserEdit }, void 0) }), void 0), _jsx(Button, __assign({ className: "p-button", onClick: function () { return deleteUser(user.id); } }, { children: _jsx(FontAwesomeIcon, { icon: faTrash }, void 0) }), void 0)] }, void 0);
            }), _jsx(Divider, {}, void 0), _jsxs(Button, __assign({ className: "p-button", onClick: function () { return props.setEditUser(null); } }, { children: [_jsx(FontAwesomeIcon, { icon: faUserPlus }, void 0), "\u00A0Create new user"] }), void 0)] }, void 0);
};
export default UserList;
