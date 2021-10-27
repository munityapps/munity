import { TypedUseSelectorHook } from 'react-redux';
import type { RootState } from './store';
export declare const useAppSelector: TypedUseSelectorHook<RootState>;
export declare const useAppDispatch: () => import("redux-thunk").ThunkDispatch<{
    app: import("./app/slice").AppState;
    layout: import("./layouts/slice").LayoutState;
    permission: import("./permissions/slice").PermissionState;
    auhentication: import("./authentication/slice").AuthenticateState;
    notification: import("./notifications/slice").NotificationState;
    user: import("@reduxjs/toolkit/dist/query/core/apiState").CombinedState<{
        getUsers: import("@reduxjs/toolkit/dist/query").QueryDefinition<void, import("@reduxjs/toolkit/dist/query").BaseQueryFn<string | import("@reduxjs/toolkit/dist/query").FetchArgs, unknown, import("@reduxjs/toolkit/dist/query").FetchBaseQueryError, {}, import("@reduxjs/toolkit/dist/query").FetchBaseQueryMeta>, "User", {
            count: number;
            results: import("./user/slice").User[];
        }, string>;
        getUser: import("@reduxjs/toolkit/dist/query").QueryDefinition<number, import("@reduxjs/toolkit/dist/query").BaseQueryFn<string | import("@reduxjs/toolkit/dist/query").FetchArgs, unknown, import("@reduxjs/toolkit/dist/query").FetchBaseQueryError, {}, import("@reduxjs/toolkit/dist/query").FetchBaseQueryMeta>, "User", import("./user/slice").User, string>;
        createUser: import("@reduxjs/toolkit/dist/query").MutationDefinition<Partial<import("./user/slice").User>, import("@reduxjs/toolkit/dist/query").BaseQueryFn<string | import("@reduxjs/toolkit/dist/query").FetchArgs, unknown, import("@reduxjs/toolkit/dist/query").FetchBaseQueryError, {}, import("@reduxjs/toolkit/dist/query").FetchBaseQueryMeta>, "User", import("./user/slice").User, "user">;
        updateUser: import("@reduxjs/toolkit/dist/query").MutationDefinition<Partial<import("./user/slice").User> & Pick<import("./user/slice").User, "id">, import("@reduxjs/toolkit/dist/query").BaseQueryFn<string | import("@reduxjs/toolkit/dist/query").FetchArgs, unknown, import("@reduxjs/toolkit/dist/query").FetchBaseQueryError, {}, import("@reduxjs/toolkit/dist/query").FetchBaseQueryMeta>, "User", import("./user/slice").User, "user">;
        deleteUser: import("@reduxjs/toolkit/dist/query").MutationDefinition<string, import("@reduxjs/toolkit/dist/query").BaseQueryFn<string | import("@reduxjs/toolkit/dist/query").FetchArgs, unknown, import("@reduxjs/toolkit/dist/query").FetchBaseQueryError, {}, import("@reduxjs/toolkit/dist/query").FetchBaseQueryMeta>, "User", void, "user">;
    }, "User", "user">;
    workspace: import("@reduxjs/toolkit/dist/query/core/apiState").CombinedState<{
        getWorkspaces: import("@reduxjs/toolkit/dist/query").QueryDefinition<void, import("@reduxjs/toolkit/dist/query").BaseQueryFn<string | import("@reduxjs/toolkit/dist/query").FetchArgs, unknown, import("@reduxjs/toolkit/dist/query").FetchBaseQueryError, {}, import("@reduxjs/toolkit/dist/query").FetchBaseQueryMeta>, "Workspace", {
            count: number;
            results: import("./workspaces/slice").Workspace[];
        }, string>;
        getWorkspace: import("@reduxjs/toolkit/dist/query").QueryDefinition<string, import("@reduxjs/toolkit/dist/query").BaseQueryFn<string | import("@reduxjs/toolkit/dist/query").FetchArgs, unknown, import("@reduxjs/toolkit/dist/query").FetchBaseQueryError, {}, import("@reduxjs/toolkit/dist/query").FetchBaseQueryMeta>, "Workspace", import("./workspaces/slice").Workspace, string>;
        createWorkspace: import("@reduxjs/toolkit/dist/query").MutationDefinition<Partial<import("./workspaces/slice").Workspace>, import("@reduxjs/toolkit/dist/query").BaseQueryFn<string | import("@reduxjs/toolkit/dist/query").FetchArgs, unknown, import("@reduxjs/toolkit/dist/query").FetchBaseQueryError, {}, import("@reduxjs/toolkit/dist/query").FetchBaseQueryMeta>, "Workspace", import("./workspaces/slice").Workspace, "workspace">;
        updateWorkspace: import("@reduxjs/toolkit/dist/query").MutationDefinition<Partial<import("./workspaces/slice").Workspace> & Pick<import("./workspaces/slice").Workspace, "slug">, import("@reduxjs/toolkit/dist/query").BaseQueryFn<string | import("@reduxjs/toolkit/dist/query").FetchArgs, unknown, import("@reduxjs/toolkit/dist/query").FetchBaseQueryError, {}, import("@reduxjs/toolkit/dist/query").FetchBaseQueryMeta>, "Workspace", import("./workspaces/slice").Workspace, "workspace">;
        deleteWorkspace: import("@reduxjs/toolkit/dist/query").MutationDefinition<string, import("@reduxjs/toolkit/dist/query").BaseQueryFn<string | import("@reduxjs/toolkit/dist/query").FetchArgs, unknown, import("@reduxjs/toolkit/dist/query").FetchBaseQueryError, {}, import("@reduxjs/toolkit/dist/query").FetchBaseQueryMeta>, "Workspace", void, "workspace">;
    }, "Workspace", "workspace">;
    settings: import("@reduxjs/toolkit/dist/query/core/apiState").CombinedState<{
        getSettings: import("@reduxjs/toolkit/dist/query").QueryDefinition<void, import("@reduxjs/toolkit/dist/query").BaseQueryFn<string | import("@reduxjs/toolkit/dist/query").FetchArgs, unknown, import("@reduxjs/toolkit/dist/query").FetchBaseQueryError, {}, import("@reduxjs/toolkit/dist/query").FetchBaseQueryMeta>, "Setting", import("./settings/slice").Setting[], string>;
        getSetting: import("@reduxjs/toolkit/dist/query").QueryDefinition<number, import("@reduxjs/toolkit/dist/query").BaseQueryFn<string | import("@reduxjs/toolkit/dist/query").FetchArgs, unknown, import("@reduxjs/toolkit/dist/query").FetchBaseQueryError, {}, import("@reduxjs/toolkit/dist/query").FetchBaseQueryMeta>, "Setting", import("./settings/slice").Setting, string>;
        createSetting: import("@reduxjs/toolkit/dist/query").MutationDefinition<Partial<import("./settings/slice").Setting>, import("@reduxjs/toolkit/dist/query").BaseQueryFn<string | import("@reduxjs/toolkit/dist/query").FetchArgs, unknown, import("@reduxjs/toolkit/dist/query").FetchBaseQueryError, {}, import("@reduxjs/toolkit/dist/query").FetchBaseQueryMeta>, "Setting", import("./settings/slice").Setting, "settings">;
        updateSetting: import("@reduxjs/toolkit/dist/query").MutationDefinition<Partial<import("./settings/slice").Setting> & Pick<import("./settings/slice").Setting, "key">, import("@reduxjs/toolkit/dist/query").BaseQueryFn<string | import("@reduxjs/toolkit/dist/query").FetchArgs, unknown, import("@reduxjs/toolkit/dist/query").FetchBaseQueryError, {}, import("@reduxjs/toolkit/dist/query").FetchBaseQueryMeta>, "Setting", import("./settings/slice").Setting, "settings">;
        deleteSetting: import("@reduxjs/toolkit/dist/query").MutationDefinition<number, import("@reduxjs/toolkit/dist/query").BaseQueryFn<string | import("@reduxjs/toolkit/dist/query").FetchArgs, unknown, import("@reduxjs/toolkit/dist/query").FetchBaseQueryError, {}, import("@reduxjs/toolkit/dist/query").FetchBaseQueryMeta>, "Setting", void, "settings">;
    }, "Setting", "settings">;
}, null, import("redux").AnyAction> & import("redux-thunk").ThunkDispatch<{
    app: import("./app/slice").AppState;
    layout: import("./layouts/slice").LayoutState;
    permission: import("./permissions/slice").PermissionState;
    auhentication: import("./authentication/slice").AuthenticateState;
    notification: import("./notifications/slice").NotificationState;
    user: import("@reduxjs/toolkit/dist/query/core/apiState").CombinedState<{
        getUsers: import("@reduxjs/toolkit/dist/query").QueryDefinition<void, import("@reduxjs/toolkit/dist/query").BaseQueryFn<string | import("@reduxjs/toolkit/dist/query").FetchArgs, unknown, import("@reduxjs/toolkit/dist/query").FetchBaseQueryError, {}, import("@reduxjs/toolkit/dist/query").FetchBaseQueryMeta>, "User", {
            count: number;
            results: import("./user/slice").User[];
        }, string>;
        getUser: import("@reduxjs/toolkit/dist/query").QueryDefinition<number, import("@reduxjs/toolkit/dist/query").BaseQueryFn<string | import("@reduxjs/toolkit/dist/query").FetchArgs, unknown, import("@reduxjs/toolkit/dist/query").FetchBaseQueryError, {}, import("@reduxjs/toolkit/dist/query").FetchBaseQueryMeta>, "User", import("./user/slice").User, string>;
        createUser: import("@reduxjs/toolkit/dist/query").MutationDefinition<Partial<import("./user/slice").User>, import("@reduxjs/toolkit/dist/query").BaseQueryFn<string | import("@reduxjs/toolkit/dist/query").FetchArgs, unknown, import("@reduxjs/toolkit/dist/query").FetchBaseQueryError, {}, import("@reduxjs/toolkit/dist/query").FetchBaseQueryMeta>, "User", import("./user/slice").User, "user">;
        updateUser: import("@reduxjs/toolkit/dist/query").MutationDefinition<Partial<import("./user/slice").User> & Pick<import("./user/slice").User, "id">, import("@reduxjs/toolkit/dist/query").BaseQueryFn<string | import("@reduxjs/toolkit/dist/query").FetchArgs, unknown, import("@reduxjs/toolkit/dist/query").FetchBaseQueryError, {}, import("@reduxjs/toolkit/dist/query").FetchBaseQueryMeta>, "User", import("./user/slice").User, "user">;
        deleteUser: import("@reduxjs/toolkit/dist/query").MutationDefinition<string, import("@reduxjs/toolkit/dist/query").BaseQueryFn<string | import("@reduxjs/toolkit/dist/query").FetchArgs, unknown, import("@reduxjs/toolkit/dist/query").FetchBaseQueryError, {}, import("@reduxjs/toolkit/dist/query").FetchBaseQueryMeta>, "User", void, "user">;
    }, "User", "user">;
    workspace: import("@reduxjs/toolkit/dist/query/core/apiState").CombinedState<{
        getWorkspaces: import("@reduxjs/toolkit/dist/query").QueryDefinition<void, import("@reduxjs/toolkit/dist/query").BaseQueryFn<string | import("@reduxjs/toolkit/dist/query").FetchArgs, unknown, import("@reduxjs/toolkit/dist/query").FetchBaseQueryError, {}, import("@reduxjs/toolkit/dist/query").FetchBaseQueryMeta>, "Workspace", {
            count: number;
            results: import("./workspaces/slice").Workspace[];
        }, string>;
        getWorkspace: import("@reduxjs/toolkit/dist/query").QueryDefinition<string, import("@reduxjs/toolkit/dist/query").BaseQueryFn<string | import("@reduxjs/toolkit/dist/query").FetchArgs, unknown, import("@reduxjs/toolkit/dist/query").FetchBaseQueryError, {}, import("@reduxjs/toolkit/dist/query").FetchBaseQueryMeta>, "Workspace", import("./workspaces/slice").Workspace, string>;
        createWorkspace: import("@reduxjs/toolkit/dist/query").MutationDefinition<Partial<import("./workspaces/slice").Workspace>, import("@reduxjs/toolkit/dist/query").BaseQueryFn<string | import("@reduxjs/toolkit/dist/query").FetchArgs, unknown, import("@reduxjs/toolkit/dist/query").FetchBaseQueryError, {}, import("@reduxjs/toolkit/dist/query").FetchBaseQueryMeta>, "Workspace", import("./workspaces/slice").Workspace, "workspace">;
        updateWorkspace: import("@reduxjs/toolkit/dist/query").MutationDefinition<Partial<import("./workspaces/slice").Workspace> & Pick<import("./workspaces/slice").Workspace, "slug">, import("@reduxjs/toolkit/dist/query").BaseQueryFn<string | import("@reduxjs/toolkit/dist/query").FetchArgs, unknown, import("@reduxjs/toolkit/dist/query").FetchBaseQueryError, {}, import("@reduxjs/toolkit/dist/query").FetchBaseQueryMeta>, "Workspace", import("./workspaces/slice").Workspace, "workspace">;
        deleteWorkspace: import("@reduxjs/toolkit/dist/query").MutationDefinition<string, import("@reduxjs/toolkit/dist/query").BaseQueryFn<string | import("@reduxjs/toolkit/dist/query").FetchArgs, unknown, import("@reduxjs/toolkit/dist/query").FetchBaseQueryError, {}, import("@reduxjs/toolkit/dist/query").FetchBaseQueryMeta>, "Workspace", void, "workspace">;
    }, "Workspace", "workspace">;
    settings: import("@reduxjs/toolkit/dist/query/core/apiState").CombinedState<{
        getSettings: import("@reduxjs/toolkit/dist/query").QueryDefinition<void, import("@reduxjs/toolkit/dist/query").BaseQueryFn<string | import("@reduxjs/toolkit/dist/query").FetchArgs, unknown, import("@reduxjs/toolkit/dist/query").FetchBaseQueryError, {}, import("@reduxjs/toolkit/dist/query").FetchBaseQueryMeta>, "Setting", import("./settings/slice").Setting[], string>;
        getSetting: import("@reduxjs/toolkit/dist/query").QueryDefinition<number, import("@reduxjs/toolkit/dist/query").BaseQueryFn<string | import("@reduxjs/toolkit/dist/query").FetchArgs, unknown, import("@reduxjs/toolkit/dist/query").FetchBaseQueryError, {}, import("@reduxjs/toolkit/dist/query").FetchBaseQueryMeta>, "Setting", import("./settings/slice").Setting, string>;
        createSetting: import("@reduxjs/toolkit/dist/query").MutationDefinition<Partial<import("./settings/slice").Setting>, import("@reduxjs/toolkit/dist/query").BaseQueryFn<string | import("@reduxjs/toolkit/dist/query").FetchArgs, unknown, import("@reduxjs/toolkit/dist/query").FetchBaseQueryError, {}, import("@reduxjs/toolkit/dist/query").FetchBaseQueryMeta>, "Setting", import("./settings/slice").Setting, "settings">;
        updateSetting: import("@reduxjs/toolkit/dist/query").MutationDefinition<Partial<import("./settings/slice").Setting> & Pick<import("./settings/slice").Setting, "key">, import("@reduxjs/toolkit/dist/query").BaseQueryFn<string | import("@reduxjs/toolkit/dist/query").FetchArgs, unknown, import("@reduxjs/toolkit/dist/query").FetchBaseQueryError, {}, import("@reduxjs/toolkit/dist/query").FetchBaseQueryMeta>, "Setting", import("./settings/slice").Setting, "settings">;
        deleteSetting: import("@reduxjs/toolkit/dist/query").MutationDefinition<number, import("@reduxjs/toolkit/dist/query").BaseQueryFn<string | import("@reduxjs/toolkit/dist/query").FetchArgs, unknown, import("@reduxjs/toolkit/dist/query").FetchBaseQueryError, {}, import("@reduxjs/toolkit/dist/query").FetchBaseQueryMeta>, "Setting", void, "settings">;
    }, "Setting", "settings">;
}, undefined, import("redux").AnyAction> & import("redux").Dispatch<import("redux").AnyAction>;
