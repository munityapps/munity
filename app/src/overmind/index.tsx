import 'react-toastify/dist/ReactToastify.css';
import { useEffect } from 'react';
import { Route, Switch } from 'react-router';
import { setWorkspace } from '../app/slice';
import { useAppDispatch } from '../hooks';
import WorkspaceList from '../workspaces/list';
import User from '../user';
import './styles.scss';
import Navbar from './components/Navbar';
import OvermindSidebar from './components/Sidebar';
import NavbarLeft from './components/NavbarComponents/NavbarLeft';
import NavbarCenter from './components/NavbarComponents/NavbarCenter';
import NavbarRight from './components/NavbarComponents/NavbarRight';
import Dashboard from './components/Dashboard';

const Overmind = (props: { newRoutes: Partial<Route>[] }) => {
    const dispatch = useAppDispatch();
    useEffect(() => {
        dispatch(setWorkspace(null));
    }, [dispatch])

    return <>
        <Navbar
            leftPart={NavbarLeft}
            centerPart={NavbarCenter}
            rightPart={NavbarRight}
        />
        <div className="layout-overmind">
            <OvermindSidebar />
            <div className="main">
                <Switch>
                    {props.newRoutes}
                    <Route path="/workspaces" component={WorkspaceList} />
                    <Route path="/users" component={User} />
                    <Route path="/" component={Dashboard} />
                </Switch>
            </div>
        </div>
    </>
}

export default Overmind;