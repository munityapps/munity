import { configureStore } from '@reduxjs/toolkit'

import coreReducer from './modules/core/slice';
import { userSlice } from './modules/user/slice';
import permissionSlice from './modules/permissions/slice';
import { workspaceSlice } from './modules/workspaces/slice';
import authenticationSlice from './modules/authentication/slice';
import notificationSlice from './modules/notifications/slice';
import { settingSlice } from './modules/settings/slice';

const store = configureStore({
    reducer: {
        core: coreReducer,
        permission: permissionSlice,
        auhentication: authenticationSlice,
        notification: notificationSlice,
        [userSlice.reducerPath] : userSlice.reducer,
        [workspaceSlice.reducerPath] : workspaceSlice.reducer,
        [settingSlice.reducerPath] : settingSlice.reducer
    },
    middleware: getDefaultMiddleware =>
        getDefaultMiddleware()
            .concat([
                userSlice.middleware,
                workspaceSlice.middleware
            ])
})

export default store;

// Infer the `RootState` and `AppDispatch` types from the store itself
export type RootState = ReturnType<typeof store.getState>
// Inferred type: {posts: PostsState, comments: CommentsState, users: UsersState}
export type AppDispatch = typeof store.dispatch