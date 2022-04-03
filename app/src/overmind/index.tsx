import 'react-toastify/dist/ReactToastify.css';
import { useEffect } from 'react';
import { Route, Switch } from 'react-router';
import { setWorkspace } from '../app/slice';
import { useAppDispatch } from '../hooks';
import WorkspaceList from '../workspaces/list';
import User from '../user';
import './styles.scss';
import Dashboard from './components/Dashboard';

const Overmind = (props: { demoMode: boolean, navbar:JSX.Element, sidebar: JSX.Element, newRoutes: Partial<Route>[] }) => {
    const dispatch = useAppDispatch();
    useEffect(() => {
        dispatch(setWorkspace(null));
    }, [dispatch])

    return <>
        {props.navbar}
        <div className="layout-overmind">
            {props.sidebar}
            <div className="main">
                <Switch>
                    {props.newRoutes}
                    { props.demoMode && <Route path="/workspaces" component={WorkspaceList} />}
                    <Route path="/users" component={User} />
                    <Route path="/" component={props.demoMode ? Dashboard : WorkspaceList} />
                </Switch>
            </div>
        </div>
    </>
}

export default Overmind;