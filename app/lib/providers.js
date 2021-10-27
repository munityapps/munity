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
import { jsx as _jsx } from "react/jsx-runtime";
// Libs
import { Provider as ReduxProvider } from 'react-redux';
import PrimeReact from 'primereact/api';
// Configuration
import store from './store';
import i18n from './i18n';
import { I18nextProvider } from 'react-i18next';
import { BrowserRouter } from 'react-router-dom';
import ThemeManager from './layouts/themeManager';
PrimeReact.ripple = true;
var Providers = function (props) {
    return _jsx(BrowserRouter, { children: _jsx(I18nextProvider, __assign({ i18n: i18n }, { children: _jsx(ReduxProvider, __assign({ store: store }, { children: _jsx(ThemeManager, { children: props.children }, void 0) }), void 0) }), void 0) }, void 0);
};
export default Providers;
