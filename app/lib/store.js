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
var store = configureStore({
    reducer: (_a = {
            app: appReducer,
            layout: layoutReducer,
            permission: permissionSlice,
            auhentication: authenticationSlice,
            notification: notificationSlice
        },
        _a[userSlice.reducerPath] = userSlice.reducer,
        _a[workspaceSlice.reducerPath] = workspaceSlice.reducer,
        _a[settingSlice.reducerPath] = settingSlice.reducer,
        _a),
    middleware: function (getDefaultMiddleware) {
        return getDefaultMiddleware()
            .concat([
            userSlice.middleware,
            workspaceSlice.middleware
        ]);
    }
});
export default store;
