import { ReactElement } from "react";
import LayoutNavbar2Columns from "../../layouts/LayoutNavbar2Columns";
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
	LayoutNavbar2Columns,
	LayoutOvermind
}

const LayoutDispatcher = ({layoutName, ...props}: LayoutDispatchConfiguration) => {
	const Layout = layoutRepository[layoutName];
	return <Layout {...props}/>
}

export default LayoutDispatcher;