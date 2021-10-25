import { ReactElement } from "react";
import TwoColumns from "../../layouts/TwoColumns";
import LayoutOvermind from "../../layouts/LayoutOvermind";

export interface LayoutConfiguration {
	mainSlot: ReactElement,
	navbarSlot?: ReactElement,
	leftPanelSlot?: ReactElement,
	rightPanelSlot?: ReactElement,
	footbarSlot?: ReactElement,
}

export interface LayoutDispatchConfiguration extends LayoutConfiguration{
	layoutName: string
}


const layoutRepository: {[key: string]: ((props: LayoutConfiguration) => ReactElement)} = {
	TwoColumns,
	LayoutOvermind
}

const LayoutDispatcher = ({layoutName, ...props}: LayoutDispatchConfiguration) => {
	const Layout = layoutRepository[layoutName];
	return <Layout {...props}/>
}

export default LayoutDispatcher;