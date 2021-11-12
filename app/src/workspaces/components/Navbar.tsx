import './Navbar.scss';
import React from 'react';

const Navbar:React.FC<{
    leftPart:React.FC
    centerPart:React.FC,
    rightPart:React.FC
}>= props => {
    return <div className="navbar">
        <props.leftPart/>
        <props.centerPart/>
        <props.rightPart/>
    </div>
};

export default Navbar;