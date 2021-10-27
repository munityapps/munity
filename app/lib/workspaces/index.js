import { jsx as _jsx, jsxs as _jsxs, Fragment as _Fragment } from "react/jsx-runtime";
import { Route, Switch, useParams } from "react-router";
import LayoutDispatcher from "../layouts/LayoutDispatcher";
import WorkspaceNavbar from "./components/WorkspaceNavbar";
import Users from "../user";
var Workspace = function () {
    var workspace_slug = useParams().workspace_slug;
    return _jsx(LayoutDispatcher, { layoutName: "TwoColumns", navbarSlot: _jsx(WorkspaceNavbar, { workspace: workspace_slug }, void 0), mainSlot: _jsx(_Fragment, { children: _jsxs(Switch, { children: [_jsx(Route, { path: "/workspace/:workspace_slug/groups", component: function () { return _jsx("div", { children: "Groups" }, void 0); } }, void 0), _jsx(Route, { path: "/workspace/:workspace_slug/users", component: Users }, void 0), _jsx(Route, { path: "/", component: function () { return _jsx("div", { children: "Welcome to worksapce " + workspace_slug }, void 0); } }, void 0)] }, void 0) }, void 0) }, void 0);
};
export default Workspace;
