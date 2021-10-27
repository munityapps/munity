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
import { jsx as _jsx, Fragment as _Fragment, jsxs as _jsxs } from "react/jsx-runtime";
import { useDeleteWorkspaceMutation, useGetWorkspacesQuery } from "./slice";
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import { Button } from "primereact/button";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faDoorOpen, faTrash } from "@fortawesome/free-solid-svg-icons";
import { useHistory } from 'react-router';
import { faEdit } from '@fortawesome/free-regular-svg-icons';
var WorkspaceList = function (props) {
    var _a = useGetWorkspacesQuery(), workspaces = _a.data, error = _a.error, isFetching = _a.isFetching, isLoading = _a.isLoading;
    var _b = useDeleteWorkspaceMutation(), deleteWorkspace = _b[0], _c = _b[1], isDeleting = _c.isLoading, deleteError = _c.isError, deleteSuccess = _c.isSuccess;
    var router = useHistory();
    var actions = function (w) { return _jsxs(_Fragment, { children: [_jsx(Button, __assign({ onClick: function () { return router.push("/workspace/" + w.slug); } }, { children: _jsx(FontAwesomeIcon, { icon: faDoorOpen }, void 0) }), void 0), _jsx(Button, __assign({ onClick: function () { return props.setEditWorkspace(w); } }, { children: _jsx(FontAwesomeIcon, { icon: faEdit }, void 0) }), void 0), _jsx(Button, __assign({ onClick: function () { return deleteWorkspace(w.slug); } }, { children: _jsx(FontAwesomeIcon, { icon: faTrash }, void 0) }), void 0)] }, void 0); };
    return _jsx("div", __assign({ className: "p-m-4" }, { children: _jsxs(DataTable, __assign({ value: workspaces === null || workspaces === void 0 ? void 0 : workspaces.results }, { children: [_jsx(Column, { field: "slug", header: "Slug" }, void 0), _jsx(Column, { field: "db_connection", header: "DBConnection" }, void 0), _jsx(Column, { body: actions, headerStyle: { width: '8em', textAlign: 'center' }, bodyStyle: { textAlign: 'center', overflow: 'visible' } }, void 0)] }), void 0) }), void 0);
};
export default WorkspaceList;
