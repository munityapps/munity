export interface LayoutState {
    primaryColor?: string;
    primaryColorText?: string;
    secondaryColor?: string;
    boxShadow?: string;
    textColor?: string;
    textColorSecondary?: string;
    contentPadding?: string;
    inlineSpacing?: string;
    surfaceA?: string;
    surfaceB?: string;
    surfaceC?: string;
    surfaceD?: string;
    errorColor?: string;
    validColor?: string;
}
export declare const layoutSlice: import("@reduxjs/toolkit").Slice<LayoutState, {}, "layout">;
declare const _default: import("redux").Reducer<LayoutState, import("redux").AnyAction>;
export default _default;
