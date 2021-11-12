import { Route, Switch, useParams } from "react-router";
import Users from "../user";
import { setWorkspace } from '../app/slice';
import React, { ComponentElement, useEffect } from "react";
import { useAppDispatch } from "../hooks";
import { Card } from 'primereact/card';

import './styles.scss';

const Workspace = (props: { navbar:Partial<React.Component>, newRoutes: Partial<Route>[] }) => {
    let { workspace_slug } = useParams<{ workspace_slug: string }>();
    const dispatch = useAppDispatch();

    useEffect(() => {
        dispatch(setWorkspace(workspace_slug));
    }, [workspace_slug, dispatch])

    return <>
        {props.navbar}
        <div className="layout-mainpage">
            <Switch>
                {props.newRoutes}
                <Route path="/workspace/:workspace_slug/users" component={Users} />
            </Switch>
        </div>
    </>
}

export default Workspace;