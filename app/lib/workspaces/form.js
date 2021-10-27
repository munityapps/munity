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
import { useCreateWorkspaceMutation, useGetWorkspacesQuery, useDeleteWorkspaceMutation, useUpdateWorkspaceMutation } from "./slice";
import { addNotification } from "../notifications/slice";
import { useAppDispatch } from "../hooks";
import { Button } from "primereact/button";
var initialWorkspaceState = {
    slug: "",
    db_connection: "",
};
export var WorkspaceForm = function (props) {
    var dispatch = useAppDispatch();
    var _a = useState(initialWorkspaceState), workspace = _a[0], setWorkspace = _a[1];
    var loadingWorkspace = useGetWorkspacesQuery().isFetching;
    var _b = useCreateWorkspaceMutation(), createWorkspace = _b[0], _c = _b[1], isCreating = _c.isLoading, createError = _c.isError, createSuccess = _c.isSuccess;
    var _d = useUpdateWorkspaceMutation(), updateWorkspace = _d[0], _e = _d[1], isUpdating = _e.isLoading, updateError = _e.isError, updateSuccess = _e.isSuccess;
    var _f = useDeleteWorkspaceMutation(), deleteWorkspace = _f[0], _g = _f[1], isDeleting = _g.isLoading, deleteError = _g.isError, deleteSuccess = _g.isSuccess;
    var handleChange = function (_a) {
        var target = _a.target;
        setWorkspace(function (prev) {
            var _a;
            return (__assign(__assign({}, prev), (_a = {}, _a[target.id] = target.value, _a)));
        });
    };
    var action = "";
    if (loadingWorkspace) {
        action = "Loading workspaces";
    }
    if (isCreating) {
        action = "Creating workspaces";
    }
    if (isUpdating) {
        action = "Updating workspaces";
    }
    if (isDeleting) {
        action = "Deleting workspaces";
    }
    useEffect(function () {
        setWorkspace(props.workspace || initialWorkspaceState);
    }, [props.workspace]);
    // Update alert
    useEffect(function () {
        if (updateError) {
            dispatch(addNotification({
                type: 'error',
                message: 'Cannot update workspace'
            }));
        }
    }, [updateError, dispatch]);
    useEffect(function () {
        if (updateSuccess) {
            dispatch(addNotification({
                type: 'success',
                message: 'Workspace updated'
            }));
        }
    }, [updateSuccess, dispatch]);
    // Delete alert
    useEffect(function () {
        if (deleteError) {
            dispatch(addNotification({
                type: 'error',
                message: 'Cannot delete workspace'
            }));
        }
    }, [deleteError, dispatch]);
    useEffect(function () {
        if (deleteSuccess) {
            dispatch(addNotification({
                type: 'success',
                message: 'Workspace deleted'
            }));
            setWorkspace(initialWorkspaceState);
        }
    }, [deleteSuccess, dispatch]);
    // Create alert
    useEffect(function () {
        if (createSuccess) {
            dispatch(addNotification({
                type: 'success',
                message: 'Workspace created'
            }));
        }
    }, [createSuccess, dispatch]);
    useEffect(function () {
        if (createError) {
            dispatch(addNotification({
                type: 'error',
                message: 'Cannot create workspace'
            }));
        }
    }, [createError, dispatch]);
    return _jsx("div", __assign({ className: "p-grid p-m-4 p-jc-between p-flex-row" }, { children: _jsxs(Fieldset, __assign({ legend: props.workspace ? "Editing workspace " + props.workspace.slug : 'Creating workspace' }, { children: [_jsxs("div", __assign({ className: "p-shadow-4 p-p-4 p-mb-4" }, { children: ["Debug action: ", action] }), void 0), _jsxs("div", __assign({ className: "p-formgrid p-grid" }, { children: [_jsxs("div", __assign({ className: "p-field p-col-12 p-md-6" }, { children: [_jsx("label", __assign({ htmlFor: "slug" }, { children: "Slug" }), void 0), _jsx(InputText, { id: "slug", onChange: handleChange, value: workspace.slug }, void 0), _jsx("br", {}, void 0)] }), void 0), _jsxs("div", __assign({ className: "p-field p-col-12 p-md-6" }, { children: [_jsx("label", __assign({ htmlFor: "db_connection" }, { children: "DB Connection" }), void 0), _jsx(InputText, { id: "db_connection", onChange: handleChange, value: workspace.db_connection }, void 0), _jsx("br", {}, void 0)] }), void 0)] }), void 0), _jsxs(Button, __assign({ onClick: function () { return props.workspace ? updateWorkspace(workspace) : createWorkspace(workspace); } }, { children: [props.workspace ? "Edit " + props.workspace.slug : 'Create workspace', " "] }), void 0), props.workspace && _jsx(Button, __assign({ onClick: function () { return deleteWorkspace(workspace.slug); } }, { children: "Delete workspace " }), void 0)] }), void 0) }), void 0);
};
