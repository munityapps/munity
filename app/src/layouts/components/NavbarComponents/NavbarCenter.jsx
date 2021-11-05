import { Button } from 'primereact/button';
import { useAppSelector } from '../../../hooks';

import { Route, Switch, useHistory, useLocation } from 'react-router';

const NavbarCenter = () => {
    const location = useLocation();
    const history = useHistory();
    const workspace_slug = useAppSelector((state) => state.app.workspace_slug);

    return <div className="middle-part">
        <Switch>
            <Route path="/workspace/:slug">
                <Button onClick={() => history.push(`/workspace/${workspace_slug}/users`)} className={`p-button-link ${location.pathname.match(/^\/workspace\/[^/]+\/users/g) ? ' active' : ''}`}>Users</Button>
                <Button onClick={() => history.push(`/workspace/${workspace_slug}/groups`)} className={`p-button-link ${location.pathname.match(/^\/workspace\/[^/]+\/groups/g) ? ' active' : ''}`}>Groups</Button>
            </Route>
            <Route path="/">
                <Button  onClick={() => history.push('/workspaces')} className={`p-button-link ${location.pathname.match(/^\/workspaces/g) ? ' active' : ''}`}>Workspaces</Button>
                <Button  onClick={() => history.push('/users')} className={`p-button-link ${location.pathname.match(/^\/users/g) ? ' active' : ''}`}>Users</Button>
            </Route>
        </Switch>
    </div>;
}

export default NavbarCenter;