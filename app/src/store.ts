import { configureStore } from '@reduxjs/toolkit'

import appReducer from './app/slice';
import layoutReducer from './layouts/slice';
import userReducer, { userAPISlice } from './user/slice';
import workspaceReducer , { workspaceAPISlice } from './workspaces/slice';
import { roleAPISlice } from './permissions/slice';
import authenticationReducer from './authentication/slice';
import notificationReducer from './notifications/slice';
import { settingAPISlice } from './settings/slice';
import { Reducer, AnyAction, Middleware, Dispatch } from 'redux';

export const munityReducer: {[key: string]:Reducer<any, AnyAction>} = {
    app: appReducer,
    layout: layoutReducer,
    authentication: authenticationReducer,
    notification: notificationReducer,
    workspace: workspaceReducer,
    user: userReducer,
    [roleAPISlice.reducerPath] : roleAPISlice.reducer,
    [userAPISlice.reducerPath] : userAPISlice.reducer,
    [workspaceAPISlice.reducerPath] : workspaceAPISlice.reducer,
    [settingAPISlice.reducerPath] : settingAPISlice.reducer
}

export const munityMiddleware: Middleware<any, any, Dispatch<AnyAction>>[] = [
    userAPISlice.middleware,
    workspaceAPISlice.middleware
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