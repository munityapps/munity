import { useEffect } from "react";
import { useAppSelector } from "../hooks";
import { ToastContainer, toast } from "react-toastify";

import 'react-toastify/dist/ReactToastify.css';
import { useTranslation } from "react-i18next";

const NotificationManager = () => {
	const newNotification = useAppSelector(state => state.notification.notif);
    const { t } = useTranslation();

	useEffect(() => {
		if (newNotification) {
			toast(newNotification.message, {
				type: newNotification.type,
				...newNotification.options
			});
		}
	}, [t, newNotification])

	return <ToastContainer theme="colored"/>
}

export default NotificationManager;