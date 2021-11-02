// Libs
import React from 'react';
import ReactDOM from 'react-dom';
import { Provider as ReduxProvider } from 'react-redux'

// Component
import Providers from './providers';
import MunityRouter from './router';

// Configuration
import reportWebVitals from './reportWebVitals';

// Style
import './styles.scss';
import store from './store';
import { Route } from 'react-router';
import OvermindNavbar from './overmind/components/OvermindNavbar';
import WorkspaceNavbar from './workspaces/components/WorkspaceNavbar';


ReactDOM.render(
    <ReduxProvider store={store}>
        <Providers>
            <React.StrictMode>
                <MunityRouter
                    // overmindNavbar={ <OvermindNavbar /> }
                    // workspaceNavbar={ <WorkspaceNavbar workspace={'asd'}/> }
                    newOvermindRoutes={[
                        <Route key={'foobar'} path="/foobar" component={() => <>OVERMIND FOOBAR</>} />
                    ]}
                    newWorkspaceRoutes={[
                        <Route key={'foobar'} path="/workspace/:workspace_slug/foobar" component={() => <>WORKSPACE FOOBAR</>} />
                    ]}
                >
                    {/* Custom routes */}
                </MunityRouter>
            </React.StrictMode>
        </Providers>
    </ReduxProvider>,
    document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals(console.log);
