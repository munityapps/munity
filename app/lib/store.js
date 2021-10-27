var _a;
import { configureStore } from '@reduxjs/toolkit';
import appReducer from './app/slice';
import layoutReducer from './layouts/slice';
import { userSlice } from './user/slice';
import permissionSlice from './permissions/slice';
import { workspaceSlice } from './workspaces/slice';
import authenticationSlice from './authentication/slice';
import notificationSlice from './notifications/slice';
import { settingSlice } from './settings/slice';
export var munityReducer = (_a = {
        app: appReducer,
        layout: layoutReducer,
        permission: permissionSlice,
        auhentication: authenticationSlice,
        notification: notificationSlice
    },
    _a[userSlice.reducerPath] = userSlice.reducer,
    _a[workspaceSlice.reducerPath] = workspaceSlice.reducer,
    _a[settingSlice.reducerPath] = settingSlice.reducer,
    _a);
export var munityMiddleware = [
    userSlice.middleware,
    workspaceSlice.middleware
];
var store = configureStore({
    reducer: munityReducer,
    middleware: function (getDefaultMiddleware) {
        return getDefaultMiddleware()
            .concat(munityMiddleware);
    }
});
export default store;
