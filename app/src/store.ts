import { configureStore } from '@reduxjs/toolkit'

import appReducer from './app/slice';
import layoutReducer from './layouts/slice';
import { userSlice } from './user/slice';
import permissionSlice from './permissions/slice';
import { workspaceSlice } from './workspaces/slice';
import authenticationSlice from './authentication/slice';
import notificationSlice from './notifications/slice';
import { settingSlice } from './settings/slice';
import { Reducer, AnyAction, Middleware, Dispatch } from 'redux';

export const munityReducer: {[key: string]:Reducer<any, AnyAction>} = {
    app: appReducer,
    layout: layoutReducer,
    permission: permissionSlice,
    auhentication: authenticationSlice,
    notification: notificationSlice,
    [userSlice.reducerPath] : userSlice.reducer,
    [workspaceSlice.reducerPath] : workspaceSlice.reducer,
    [settingSlice.reducerPath] : settingSlice.reducer
}

export const munityMiddleware: Middleware<any, any, Dispatch<AnyAction>>[] = [
    userSlice.middleware,
    workspaceSlice.middleware
]

const store = configureStore({
    reducer: munityReducer,
    middleware: getDefaultMiddleware =>
        getDefaultMiddleware()
            .concat(munityMiddleware)
})

export default store;

// Infer the `RootState` and `AppDispatch` types from the store itself
export type RootState = ReturnType<typeof store.getState>
// Inferred type: {posts: PostsState, comments: CommentsState, users: UsersState}
export type AppDispatch = typeof store.dispatch