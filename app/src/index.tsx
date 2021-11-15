// Libs
import React from 'react';
import ReactDOM from 'react-dom';
import { Provider as ReduxProvider } from 'react-redux'

// Component
import Providers from './providers';
import MunityApp from './app';
import Navbar from './workspaces/components/Navbar';
import LoadingMunity from './layouts/components/LoadingMunity';

// Configuration
import reportWebVitals from './reportWebVitals';

// Style
import './styles.scss';
import store from './store';
import { Route } from 'react-router';
import NavbarLeft from './workspaces/components/NavbarComponents/NavbarLeft';
import NavbarCenter from './workspaces/components/NavbarComponents/NavbarCenter';
import NavbarRight from './workspaces/components/NavbarComponents/NavbarRight';
import OvermindSidebar from './overmind/components/Sidebar';
import { Button } from 'primereact/button';

ReactDOM.render(
    <ReduxProvider store={store}>
        <Providers>
            <React.StrictMode>
                <MunityApp
                    workspaceNavbar={<Navbar
                        leftPart={NavbarLeft}
                        centerPart={NavbarCenter}
                        rightPart={NavbarRight}
                    />}
                    overmindSidebar={<OvermindSidebar newMenuButton={[
                        // <div className="menu">
                        //     <Button className="p-button-link ">
                        //         Integration 2
                        //     </Button>
                        // </div>
                    ]}/>}
                    newOvermindRoutes={[
                        <Route key={'foobar'} path="/foobar" component={() => <>OVERMIND FOOBAR</>} />
                    ]}
                    newWorkspaceRoutes={[
                        <Route key={'foobar'} path="/workspace/:workspace_slug/foobar" component={() => <>WORKSPACE FOOBAR</>} />
                    ]}
                    loadingWorkspace={LoadingMunity}
                >
                    {/* Custom routes */}
                </MunityApp>
            </React.StrictMode>
        </Providers>
    </ReduxProvider>,
    document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals(console.log);
