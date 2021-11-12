import { Button } from 'primereact/button';

import { Route, Switch } from 'react-router';
import { useAppDispatch } from '../../../hooks';
import { addNotification } from '../../../notifications/slice';

import munityLogo from '../../../assets/logoIcon.png';

const NavbarCenter = () => {
    const dispatch = useAppDispatch();
    const featureInative = () => {
        dispatch(addNotification({
            type: 'info',
            message: <div style={{display:'flex', alignItems: 'center'}}>
                <img style={{height:'60px'}} src={munityLogo} alt="munityLogo"/>
                <div>You need <a href="https://munityapps.com">
                    Munity Portal</a> to access this feature.
                </div>
            </div>
        }));
    };

    return <div className="middle-part">
        <Switch>
            <Route path="/">
                <Button onClick={featureInative} className={`p-button-link`}>Projects</Button>
                <Button onClick={featureInative} className={`p-button-link`}>Boilerplates</Button>
                <Button onClick={featureInative} className={`p-button-link`}>Developers</Button>
                <Button onClick={featureInative} className={`p-button-link`}>Learn</Button>
                <Button onClick={featureInative} className={`p-button-link`}>Feed</Button>
            </Route>
        </Switch>
    </div>;
}

export default NavbarCenter;