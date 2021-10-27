export interface AuthenticateState {
    pending: boolean;
    access: string | null;
    refresh: string | null;
}
export declare const authenticate: import("@reduxjs/toolkit").AsyncThunk<{
    access: any;
    refresh: any;
}, {
    username: string;
    password: string;
}, {}>;
export declare const permissionSlice: import("@reduxjs/toolkit").Slice<AuthenticateState, {
    logout: (state: import("immer/dist/internal").WritableDraft<AuthenticateState>) => void;
}, "authentication">;
export declare const logout: import("@reduxjs/toolkit").ActionCreatorWithoutPayload<string>;
declare const _default: import("redux").Reducer<AuthenticateState, import("redux").AnyAction>;
export default _default;
