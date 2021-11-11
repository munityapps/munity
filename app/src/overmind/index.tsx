import 'react-toastify/dist/ReactToastify.css';
import { useEffect } from 'react';
import { Route, Switch } from 'react-router';
import { setWorkspace } from '../app/slice';
import { useAppDispatch } from '../hooks';
import WorkspaceList from '../workspaces/list';
import overmindLogo from '../assets/overmind.png';
import User from '../user';
import './styles.scss';

const Overmind = (props: { newRoutes: Partial<Route>[] }) => {
    const dispatch = useAppDispatch();
    useEffect(() => {
        dispatch(setWorkspace(null));
    }, [dispatch])

    return <div className="layout-mainpage">
        <Switch>
            {props.newRoutes}
            <Route path="/workspaces" component={WorkspaceList} />
            <Route path="/users" component={User} />
            <Route path="/" component={() => <div className="mainpage-root">
                <img className="logo-overmind" src={overmindLogo} alt="this is overmind"/>
            </div>} />
        </Switch>
    </div>
}

export default Overmind;