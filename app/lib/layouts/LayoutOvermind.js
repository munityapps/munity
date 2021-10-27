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
import './LayoutOvermind.scss';
var LayoutOvermind = function (props) {
    return _jsxs("div", __assign({ className: "layout-overmind-navbar" }, { children: [_jsx("div", __assign({ className: "top" }, { children: props.navbarSlot || null }), void 0), _jsx("div", __assign({ className: "center" }, { children: props.mainSlot || null }), void 0)] }), void 0);
};
export default LayoutOvermind;
