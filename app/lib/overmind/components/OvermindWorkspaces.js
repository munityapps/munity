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
import { useState } from 'react';
import { useDeleteWorkspaceMutation, useGetWorkspacesQuery } from "../../workspaces/slice";
import { Button } from "primereact/button";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faDoorOpen, faTrash } from "@fortawesome/free-solid-svg-icons";
import { WorkspaceForm } from "../../workspaces/form";
import { useHistory } from 'react-router';
import { faEdit } from '@fortawesome/free-regular-svg-icons';
import LayoutDispatcher from '../../layouts/LayoutDispatcher';
import WorkspaceList from '../../workspaces/list';
var OvermindWorkspaces = function () {
    var _a = useGetWorkspacesQuery(), workspaces = _a.data, error = _a.error, isFetching = _a.isFetching, isLoading = _a.isLoading;
    var _b = useDeleteWorkspaceMutation(), deleteWorkspace = _b[0], _c = _b[1], isDeleting = _c.isLoading, deleteError = _c.isError, deleteSuccess = _c.isSuccess;
    var _d = useState(null), editWorkspace = _d[0], setEditWorkspace = _d[1];
    var router = useHistory();
    var actions = function (w) { return _jsxs(_Fragment, { children: [_jsx(Button, __assign({ onClick: function () { return router.push("/workspace/" + w.slug); } }, { children: _jsx(FontAwesomeIcon, { icon: faDoorOpen }, void 0) }), void 0), _jsx(Button, __assign({ onClick: function () { return setEditWorkspace(w); } }, { children: _jsx(FontAwesomeIcon, { icon: faEdit }, void 0) }), void 0), _jsx(Button, __assign({ onClick: function () { return deleteWorkspace(w.slug); } }, { children: _jsx(FontAwesomeIcon, { icon: faTrash }, void 0) }), void 0)] }, void 0); };
    // return <div className="p-m-4">
    //     {
    //     }
    //     <WorkspaceForm setEditWorkspace={setEditWorkspace} workspace={editWorkspace} />
    // </div>;
    return _jsx(LayoutDispatcher, { layoutName: "TwoColumns", mainSlot: _jsx(WorkspaceForm, { workspace: editWorkspace }, void 0), rightPanelSlot: _jsx(WorkspaceList, { setEditWorkspace: setEditWorkspace }, void 0) }, void 0);
};
export default OvermindWorkspaces;
