import { Route, Switch, useParams } from "react-router";
import LayoutDispatcher from "../core/components/LayoutDispatcher";
import WorkspaceNavbar from "./components/WorkspaceNavbar";
import Users from "../user";

const Workspace = () => {
    let { workspace_slug } = useParams<{ workspace_slug: string }>();
    return <LayoutDispatcher
        layoutName="TwoColumns"
		navbarSlot={<WorkspaceNavbar workspace={workspace_slug}/>}
        mainSlot={<>
            <Switch>
                <Route path="/workspace/:workspace_slug/groups" component={() => <div>Groups</div>} />
                <Route path="/workspace/:workspace_slug/users" component={Users} />
                <Route path="/" component={() => <div>{`Welcome to worksapce ${workspace_slug}`}</div>} />
            </Switch>
        </>}
    />
}

export default Workspace;