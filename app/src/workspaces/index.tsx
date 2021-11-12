import { Route, Switch, useParams } from "react-router";
import Users from "../user";
import { setWorkspace } from '../app/slice';
import { useEffect } from "react";
import { useAppDispatch } from "../hooks";
import { Card } from 'primereact/card';

import './styles.scss';

const Workspace = (props: { newRoutes: Partial<Route>[] }) => {
    let { workspace_slug } = useParams<{ workspace_slug: string }>();
    const dispatch = useAppDispatch();

    useEffect(() => {
        dispatch(setWorkspace(workspace_slug));
    }, [workspace_slug, dispatch])

    return <div className="layout-mainpage">
        <Switch>
            {props.newRoutes}
            <Route path="/workspace/:workspace_slug/groups" component={() => <div>Groups</div>} />
            <Route path="/workspace/:workspace_slug/users" component={Users} />
            <Route path="/workspace/" component={() => <div className="mainpage-root">
                <Card className="p-shadow-2">
                    {`Welcome to workspace ${workspace_slug}`}
                </Card>
            </div>} />
        </Switch>
    </div>
}

export default Workspace;