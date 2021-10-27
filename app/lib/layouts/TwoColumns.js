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
import './TwoColumns.scss';
var TwoColumns = function (props) {
    // const { t } = useTranslation();
    return _jsxs("div", __assign({ className: "layout-navbar-2-columns p-d-flex p-flex-column" }, { children: [props.navbarSlot, _jsxs("div", __assign({ className: 'p-d-flex p-flex-row main-content' }, { children: [_jsx("div", __assign({ className: "left-column p-d-flex p-ai-center p-jc-center" }, { children: props.mainSlot }), void 0), _jsx("div", __assign({ className: "right-column p-d-flex p-ai-center p-jc-center" }, { children: props.rightPanelSlot }), void 0)] }), void 0)] }), void 0);
};
export default TwoColumns;
