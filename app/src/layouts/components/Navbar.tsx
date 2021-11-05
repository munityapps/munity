import './Navbar.scss';
import { FunctionComponent } from 'react';

const Navbar = (props:{
    leftPart:FunctionComponent,
    centerPart:FunctionComponent,
    rightPart:FunctionComponent
}) => {
    return <div className="navbar">
        <props.leftPart/>
        <props.centerPart/>
        <props.rightPart/>
    </div>
};

export default Navbar;