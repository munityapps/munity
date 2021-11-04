import { Route, Switch, useParams } from "react-router";
import Users from "../user";
import { setWorkspace } from '../app/slice';
import { useEffect } from "react";
import { useAppDispatch } from "../hooks";

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
            <Route path="/" component={() => <div className="mainpage-root">{`Welcome to worksapce ${workspace_slug}`}</div>} />
        </Switch>
    </div>
}

export default Workspace;