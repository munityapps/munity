import { LayoutConfiguration } from '../layouts/LayoutDispatcher';
import './LayoutOvermind.scss';

const LayoutOvermind = (props: LayoutConfiguration) => {
    return <div className="layout-overmind-navbar">
        <div className="top">
            {props.navbarSlot || null}
        </div>
        <div className="center">
            {props.mainSlot || null}
        </div>
    </div>
}

export default LayoutOvermind;

