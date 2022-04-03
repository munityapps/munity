import React from 'react';
import Workspace from '../workspaces';
import Overmind from '../overmind';
import { Route, Switch } from 'react-router';

const AppRouter: React.FC<{
    children: object,
    demoMode: boolean,
    loadingWorkspace: React.FC,
    overmindSidebar: JSX.Element,
    workspaceNavbar: JSX.Element,
    overmindNavbar: JSX.Element,
    newOvermindRoutes: Partial<Route>[],
    newWorkspaceRoutes: Partial<Route>[]
}> = props => {

    // Main Munity router
    return <>
        <Switch>
            {props.children}
            <Route path="/workspace/:workspace_slug" children={<Workspace demoMode={props.demoMode} navbar={props.workspaceNavbar} newRoutes={props.newWorkspaceRoutes} />} />
            <Route path="/" children={<Overmind demoMode={props.demoMode} navbar={props.overmindNavbar} sidebar={props.overmindSidebar} newRoutes={props.newOvermindRoutes} />} />
        </Switch>
    </>;
}

export default AppRouter;