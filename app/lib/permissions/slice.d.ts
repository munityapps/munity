interface Perm {
    role: string;
    action: string;
    filter: object;
}
export interface PermissionState {
    perms: Array<Perm>;
}
export declare const permissionSlice: import("@reduxjs/toolkit").Slice<PermissionState, {
    setPerms: (state: import("immer/dist/internal").WritableDraft<PermissionState>, action: {
        payload: any;
        type: string;
    }) => void;
}, "permission">;
export declare const setPerms: import("@reduxjs/toolkit").ActionCreatorWithPayload<any, string>;
declare const _default: import("redux").Reducer<PermissionState, import("redux").AnyAction>;
export default _default;
