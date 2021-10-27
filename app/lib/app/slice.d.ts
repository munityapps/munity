export interface AppState {
    isReady: boolean;
    loading: boolean;
    resourceLoaded: boolean;
}
export declare const appSlice: import("@reduxjs/toolkit").Slice<AppState, {
    ready: (state: import("immer/dist/internal").WritableDraft<AppState>) => void;
    resourceLoaded: (state: import("immer/dist/internal").WritableDraft<AppState>) => void;
}, "app">;
export declare const ready: import("@reduxjs/toolkit").ActionCreatorWithoutPayload<string>, resourceLoaded: import("@reduxjs/toolkit").ActionCreatorWithoutPayload<string>;
declare const _default: import("redux").Reducer<AppState, import("redux").AnyAction>;
export default _default;
