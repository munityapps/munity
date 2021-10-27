import { jsx as _jsx } from "react/jsx-runtime";
import LayoutDispatcher from "../layouts/LayoutDispatcher";
import { UserForm } from "./form";
import { useState } from "react";
import UserList from "./list";
var Users = function () {
    var _a = useState(null), editUser = _a[0], setEditUser = _a[1];
    return _jsx(LayoutDispatcher, { layoutName: "TwoColumns", mainSlot: _jsx(UserForm, { user: editUser }, void 0), rightPanelSlot: _jsx(UserList, { setEditUser: setEditUser }, void 0) }, void 0);
};
export default Users;
