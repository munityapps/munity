
import { Route, Switch } from 'react-router';
import 'react-toastify/dist/ReactToastify.css';
import LayoutDispatcher from '../layouts/LayoutDispatcher';
import User from '../user';
import Navbar from './components/OvermindNavbar';
import OvermindWorkspaces from './components/OvermindWorkspaces';

const Overmind = (props: {newRoutes: Partial<Route>[]}) => {
    return <LayoutDispatcher
        layoutName="TwoColumns"
        navbarSlot={<Navbar />}
        mainSlot={<>
            <Switch>
                {props.newRoutes}
                <Route path="/workspaces" component={OvermindWorkspaces} />
                <Route path="/users" component={User} />
                <Route path="/" component={() => <div>This is overmind !</div>} />
            </Switch>
        </>}
    />
}

export default Overmind;