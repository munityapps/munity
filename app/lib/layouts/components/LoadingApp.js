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
import logo from '../../assets/logo.png';
import { ProgressSpinner } from 'primereact/progressspinner';
var LoadingApp = function () {
    return _jsxs("div", __assign({ className: "app-loading" }, { children: [_jsx("img", { src: logo, alt: "Logo" }, void 0), _jsx(ProgressSpinner, {}, void 0)] }), void 0);
};
export default LoadingApp;
