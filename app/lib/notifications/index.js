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
import { useEffect } from "react";
import { useAppSelector } from "../hooks";
import { ToastContainer, toast } from "react-toastify";
import 'react-toastify/dist/ReactToastify.css';
import { useTranslation } from "react-i18next";
var NotificationManager = function () {
    var newNotification = useAppSelector(function (state) { return state.notification.notif; });
    var t = useTranslation().t;
    useEffect(function () {
        if (newNotification) {
            toast(t(newNotification.message), __assign({ type: newNotification.type }, newNotification.options));
        }
    }, [t, newNotification]);
    return _jsx(ToastContainer, { theme: "colored" }, void 0);
};
export default NotificationManager;
