import { ReactElement } from "react";
export interface LayoutConfiguration {
    mainSlot: ReactElement;
    navbarSlot?: ReactElement;
    leftPanelSlot?: ReactElement;
    rightPanelSlot?: ReactElement;
    footbarSlot?: ReactElement;
}
export interface LayoutDispatchConfiguration extends LayoutConfiguration {
    layoutName: string;
}
declare const LayoutDispatcher: ({ layoutName, ...props }: LayoutDispatchConfiguration) => JSX.Element;
export default LayoutDispatcher;
