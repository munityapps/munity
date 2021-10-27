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
import { jsxs as _jsxs, jsx as _jsx } from "react/jsx-runtime";
import { useState, useEffect } from "react";
import { InputText } from "primereact/inputtext";
import { Fieldset } from "primereact/fieldset";
import { useCreateUserMutation, useGetUsersQuery, useDeleteUserMutation, useUpdateUserMutation } from "./slice";
import { addNotification } from "../notifications/slice";
import { useAppDispatch } from "../hooks";
import { Button } from "primereact/button";
var initialUserState = {
    id: "",
    username: "",
    first_name: "",
    last_name: "",
    email: "",
    generic_groups: [],
    roles: []
};
export var UserForm = function (props) {
    var dispatch = useAppDispatch();
    var _a = useState(initialUserState), user = _a[0], setUser = _a[1];
    var loadingUser = useGetUsersQuery().isFetching;
    var _b = useCreateUserMutation(), createUser = _b[0], _c = _b[1], isCreating = _c.isLoading, createError = _c.isError, createSuccess = _c.isSuccess;
    var _d = useUpdateUserMutation(), updateUser = _d[0], _e = _d[1], isUpdating = _e.isLoading, updateError = _e.isError, updateSuccess = _e.isSuccess;
    var _f = useDeleteUserMutation(), deleteUser = _f[0], _g = _f[1], isDeleting = _g.isLoading, deleteError = _g.isError, deleteSuccess = _g.isSuccess;
    var handleChange = function (_a) {
        var target = _a.target;
        setUser(function (prev) {
            var _a;
            return (__assign(__assign({}, prev), (_a = {}, _a[target.id] = target.value, _a)));
        });
    };
    var action = "";
    if (loadingUser) {
        action = "Loading users";
    }
    if (isCreating) {
        action = "Creating users";
    }
    if (isUpdating) {
        action = "Updating users";
    }
    if (isDeleting) {
        action = "Deleting users";
    }
    useEffect(function () {
        setUser(props.user || initialUserState);
    }, [props.user]);
    // Update alert
    useEffect(function () {
        if (updateError) {
            dispatch(addNotification({
                type: 'error',
                message: 'Cannot update user'
            }));
        }
    }, [updateError, dispatch]);
    useEffect(function () {
        if (updateSuccess) {
            dispatch(addNotification({
                type: 'success',
                message: 'User updated'
            }));
        }
    }, [updateSuccess, dispatch]);
    // Delete alert
    useEffect(function () {
        if (deleteError) {
            dispatch(addNotification({
                type: 'error',
                message: 'Cannot delete user'
            }));
        }
    }, [deleteError, dispatch]);
    useEffect(function () {
        if (deleteSuccess) {
            dispatch(addNotification({
                type: 'success',
                message: 'User deleted'
            }));
            setUser(initialUserState);
        }
    }, [deleteSuccess, dispatch]);
    // Create alert
    useEffect(function () {
        if (createSuccess) {
            dispatch(addNotification({
                type: 'success',
                message: 'User created'
            }));
        }
    }, [createSuccess, dispatch]);
    useEffect(function () {
        if (createError) {
            dispatch(addNotification({
                type: 'error',
                message: 'Cannot create user'
            }));
        }
    }, [createError, dispatch]);
    return _jsx("div", __assign({ className: "p-grid p-m-4 p-jc-between p-flex-row" }, { children: _jsxs(Fieldset, __assign({ legend: props.user ? "Editing user " + props.user.username : 'Creating user' }, { children: [_jsxs("div", __assign({ className: "p-shadow-4 p-p-4 p-mb-4" }, { children: ["Debug action: ", action] }), void 0), _jsxs("div", __assign({ className: "p-formgrid p-grid" }, { children: [_jsxs("div", __assign({ className: "p-field p-col-12 p-md-6" }, { children: [_jsx("label", __assign({ htmlFor: "username" }, { children: "Username" }), void 0), _jsx(InputText, { id: "username", onChange: handleChange, value: user.username }, void 0), _jsx("br", {}, void 0)] }), void 0), _jsxs("div", __assign({ className: "p-field p-col-12 p-md-6" }, { children: [_jsx("label", __assign({ htmlFor: "first_name" }, { children: "Firstname" }), void 0), _jsx(InputText, { id: "first_name", onChange: handleChange, value: user.first_name }, void 0), _jsx("br", {}, void 0)] }), void 0), _jsxs("div", __assign({ className: "p-field p-col-12 p-md-6" }, { children: [_jsx("label", __assign({ htmlFor: "first_name" }, { children: "Lastname" }), void 0), _jsx(InputText, { id: "last_name", onChange: handleChange, value: user.last_name }, void 0), _jsx("br", {}, void 0)] }), void 0), _jsxs("div", __assign({ className: "p-field p-col-12 p-md-6" }, { children: [_jsx("label", __assign({ htmlFor: "email" }, { children: "Email" }), void 0), _jsx(InputText, { id: "email", onChange: handleChange, value: user.email }, void 0), _jsx("br", {}, void 0)] }), void 0), _jsxs("div", __assign({ className: "p-field p-col-12 p-md-6" }, { children: [_jsx("label", __assign({ htmlFor: "email" }, { children: "Groups" }), void 0), _jsx(InputText, { id: "generic_groups", onChange: handleChange, value: user.generic_groups }, void 0), _jsx("br", {}, void 0)] }), void 0), _jsxs("div", __assign({ className: "p-field p-col-12 p-md-6" }, { children: [_jsx("label", __assign({ htmlFor: "email" }, { children: "Roles" }), void 0), _jsx(InputText, { id: "roles", value: user.roles }, void 0), _jsx("br", {}, void 0)] }), void 0)] }), void 0), _jsxs(Button, __assign({ onClick: function () { return props.user ? updateUser(user) : createUser(user); } }, { children: [props.user ? "Edit " + props.user.username : 'Create user', " "] }), void 0), props.user && _jsx(Button, __assign({ onClick: function () { return deleteUser(user.id); } }, { children: "Delete user " }), void 0)] }), void 0) }), void 0);
};
