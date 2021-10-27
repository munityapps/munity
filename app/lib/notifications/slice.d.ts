interface NotificationPayload {
    type: 'warning' | 'error' | 'info' | 'success';
    message: string;
    options?: object;
}
export interface NotificationState {
    notif: NotificationPayload | null;
}
export declare const coreSlice: import("@reduxjs/toolkit").Slice<NotificationState, {
    addNotification: (state: NotificationState, action: {
        payload: NotificationPayload;
        type: string;
    }) => void;
}, "notifications">;
export declare const addNotification: import("@reduxjs/toolkit").ActionCreatorWithPayload<NotificationPayload, string>;
declare const _default: import("redux").Reducer<NotificationState, import("redux").AnyAction>;
export default _default;
